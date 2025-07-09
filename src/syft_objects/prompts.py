# syft-objects prompts - Interactive prompts with timeout support

import sys
import time
from typing import Optional
import threading
import queue


def is_jupyter_environment() -> bool:
    """Detect if we're running in a Jupyter environment"""
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            return True
    except ImportError:
        pass
    return False


def is_colab_environment() -> bool:
    """Detect if we're running in Google Colab"""
    try:
        import google.colab
        return True
    except ImportError:
        return False


def prompt_with_timeout(
    message: str, 
    timeout: float = 2.0, 
    jupyter_compatible: bool = True,
    accept_value: Optional[str] = None
) -> Optional[str]:
    """
    Show a prompt with timeout that works in both terminal and Jupyter.
    
    Args:
        message: The message to show
        timeout: Seconds to wait before auto-skip
        jupyter_compatible: Whether to use Jupyter-specific UI
        accept_value: The value to return if accepted (defaults to message)
        
    Returns:
        The accept_value if user accepts, None if timeout or skipped
    """
    if accept_value is None:
        accept_value = message
    
    in_jupyter = is_jupyter_environment()
    in_colab = is_colab_environment()
    
    # Use appropriate method based on environment
    if in_colab:
        # Colab doesn't support widgets well, use simple approach
        return _terminal_prompt(message, timeout, accept_value)
    elif in_jupyter and jupyter_compatible:
        try:
            return _jupyter_prompt(message, timeout, accept_value)
        except Exception:
            # Fall back to terminal if widgets fail
            return _terminal_prompt(message, timeout, accept_value)
    else:
        return _terminal_prompt(message, timeout, accept_value)


def _jupyter_prompt(message: str, timeout: float, accept_value: str) -> Optional[str]:
    """Jupyter-specific prompt using ipywidgets"""
    try:
        from IPython.display import display, clear_output, HTML
        import ipywidgets as widgets
        
        # Create widgets
        container = widgets.VBox()
        label = widgets.HTML(f"<b>📊 {message}</b>")
        
        # Create buttons
        button_box = widgets.HBox()
        accept_btn = widgets.Button(
            description="✓ Accept", 
            button_style='success',
            layout=widgets.Layout(width='100px')
        )
        skip_btn = widgets.Button(
            description="⏭ Skip", 
            button_style='warning',
            layout=widgets.Layout(width='100px')
        )
        button_box.children = [accept_btn, skip_btn]
        
        # Progress bar
        progress = widgets.IntProgress(
            value=0,
            min=0,
            max=int(timeout * 10),  # 10 updates per second
            description='Time:',
            bar_style='info'
        )
        
        # Status label
        status = widgets.HTML(f"<i>Waiting... ({timeout}s timeout)</i>")
        
        # Assemble container
        container.children = [label, button_box, progress, status]
        
        # Display it
        display(container)
        
        # Track state
        result = {"done": False, "accepted": False}
        
        def on_accept(b):
            if not result["done"]:
                result["done"] = True
                result["accepted"] = True
                accept_btn.disabled = True
                skip_btn.disabled = True
                status.value = "<b style='color: green'>✓ Accepted!</b>"
        
        def on_skip(b):
            if not result["done"]:
                result["done"] = True
                result["accepted"] = False
                accept_btn.disabled = True
                skip_btn.disabled = True
                status.value = "<b style='color: orange'>⏭ Skipped!</b>"
        
        accept_btn.on_click(on_accept)
        skip_btn.on_click(on_skip)
        
        # Use IPython's event loop processing
        import time
        from IPython import get_ipython
        
        start = time.time()
        ipython = get_ipython()
        
        while time.time() - start < timeout and not result["done"]:
            elapsed = time.time() - start
            remaining = max(0, timeout - elapsed)
            
            # Update progress
            progress.value = int(elapsed * 10)
            status.value = f"<i>Waiting... ({remaining:.1f}s remaining)</i>"
            
            # Process events to allow button clicks
            if ipython and hasattr(ipython, 'kernel'):
                ipython.kernel.do_one_iteration()
            else:
                # Fallback for non-kernel environments
                time.sleep(0.01)
        
        # Timeout handling
        if not result["done"]:
            result["done"] = True
            accept_btn.disabled = True
            skip_btn.disabled = True
            status.value = "<b style='color: gray'>⏱ Timed out!</b>"
            time.sleep(0.5)  # Brief pause to show timeout
        
        # Clear display
        clear_output()
        
        # Return result
        if result["accepted"]:
            print(f"✓ Mock note added: {accept_value}")
            return accept_value
        else:
            print("⏱️  No mock note added")
            return None
            
    except Exception as e:
        # Fall back to terminal prompt
        print(f"Widget error: {e}, falling back to terminal prompt")
        return _terminal_prompt(message, timeout, accept_value)


def _terminal_prompt(message: str, timeout: float, accept_value: str) -> Optional[str]:
    """Terminal prompt with timeout using threading"""
    print(f"\n📊 {message}")
    print(f"Press Enter to accept, or wait {timeout}s to skip...")
    
    # Use threading for non-blocking input with timeout
    result_queue = queue.Queue()
    
    def get_input():
        try:
            # For Windows compatibility
            if sys.platform == 'win32':
                import msvcrt
                start_time = time.time()
                while time.time() - start_time < timeout:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key in [b'\r', b'\n']:  # Enter key
                            result_queue.put(True)
                            return
                    time.sleep(0.1)
                result_queue.put(False)
            else:
                # Unix-like systems
                import select
                ready, _, _ = select.select([sys.stdin], [], [], timeout)
                if ready:
                    sys.stdin.readline()
                    result_queue.put(True)
                else:
                    result_queue.put(False)
        except Exception:
            result_queue.put(False)
    
    # Start input thread
    input_thread = threading.Thread(target=get_input, daemon=True)
    input_thread.start()
    
    # Wait for result or timeout
    try:
        accepted = result_queue.get(timeout=timeout + 0.5)
    except queue.Empty:
        accepted = False
    
    if accepted:
        print(f"✓ Mock note added: {accept_value}")
        return accept_value
    else:
        print("⏱️  Timeout - no mock note added")
        return None


def simple_prompt(message: str, default: str = "") -> str:
    """Simple blocking prompt without timeout"""
    try:
        response = input(f"{message} [{default}]: ").strip()
        return response if response else default
    except (KeyboardInterrupt, EOFError):
        return default