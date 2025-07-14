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
        from IPython.display import display, clear_output
        import ipywidgets as widgets
        import asyncio
        import time
        
        # Simple approach: Just display the widgets and wait
        label = widgets.HTML(f"<h4>📊 {message}</h4>")
        
        accept_btn = widgets.Button(
            description="✓ Accept", 
            button_style='success',
            layout=widgets.Layout(width='120px')
        )
        skip_btn = widgets.Button(
            description="⏭ Skip", 
            button_style='warning',
            layout=widgets.Layout(width='120px')
        )
        
        progress = widgets.FloatProgress(
            value=0.0,
            min=0.0,
            max=timeout,
            description='Time:',
            bar_style='info'
        )
        
        output = widgets.Output()
        
        # Layout
        ui = widgets.VBox([
            label,
            widgets.HBox([accept_btn, skip_btn]),
            progress,
            output
        ])
        
        # State
        result = {"value": None}
        
        def on_accept(b):
            result["value"] = "accept"
            accept_btn.disabled = True
            skip_btn.disabled = True
            with output:
                print("✓ Accepted!")
        
        def on_skip(b):
            result["value"] = "skip"
            accept_btn.disabled = True
            skip_btn.disabled = True
            with output:
                print("⏭ Skipped!")
        
        accept_btn.on_click(on_accept)
        skip_btn.on_click(on_skip)
        
        # Display the UI
        display(ui)
        
        # Simple polling loop with asyncio
        async def wait_for_result():
            start = time.time()
            while result["value"] is None:
                elapsed = time.time() - start
                if elapsed >= timeout:
                    break
                
                progress.value = elapsed
                progress.description = f'{timeout - elapsed:.1f}s'
                
                # Critical: yield control to allow events to process
                await asyncio.sleep(0.05)
            
            # Timeout cleanup
            if result["value"] is None:
                accept_btn.disabled = True
                skip_btn.disabled = True
                with output:
                    print("⏱ Timed out!")
        
        # Run the async function properly in Jupyter
        try:
            # In Jupyter, we can't use run_until_complete because the loop is already running
            # Instead, we need to schedule the coroutine and wait synchronously
            loop = asyncio.get_event_loop()
            
            if loop.is_running():
                # We're in Jupyter - use ensure_future and wait manually
                task = asyncio.ensure_future(wait_for_result())
                
                # Manual wait loop that processes events
                start = time.time()
                while not task.done() and (time.time() - start) < timeout + 0.5:
                    time.sleep(0.01)  # Very short sleep
                    # This allows the event loop to process widget events
            else:
                # Standard Python - run normally
                loop.run_until_complete(wait_for_result())
                
        except Exception as e:
            # Fallback: just wait with timeout
            print(f"Async error: {e}")
            time.sleep(timeout)
        
        # Clear display
        clear_output()
        
        # Return result
        if result["value"] == "accept":
            print(f"✓ Mock note added: {accept_value}")
            return accept_value
        else:
            print("No mock note added")
            return None
            
    except Exception as e:
        # Fall back to simple timeout
        print(f"Widget error: {e}")
        print(f"Mock note suggestion: {accept_value}")
        print(f"Waiting {timeout}s (buttons not available due to environment limitations)...")
        time.sleep(timeout)
        print("⏱️  Timeout - no mock note added")
        return None


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