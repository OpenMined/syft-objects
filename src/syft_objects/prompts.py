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
        import threading
        import time
        
        # Create output widget for clean display
        output = widgets.Output()
        
        with output:
            # Create widgets
            label = widgets.HTML(f"<h4>📊 {message}</h4>")
            
            # Create buttons with better styling
            accept_btn = widgets.Button(
                description="✓ Accept", 
                button_style='success',
                layout=widgets.Layout(width='120px', height='35px'),
                style={'font_weight': 'bold'}
            )
            skip_btn = widgets.Button(
                description="⏭ Skip", 
                button_style='warning',
                layout=widgets.Layout(width='120px', height='35px'),
                style={'font_weight': 'bold'}
            )
            
            # Progress bar
            progress = widgets.IntProgress(
                value=0,
                min=0,
                max=100,
                description='Time:',
                bar_style='info',
                orientation='horizontal',
                layout=widgets.Layout(width='300px')
            )
            
            # Status label
            status_label = widgets.Label(
                value=f'Waiting {timeout}s...',
                layout=widgets.Layout(width='300px')
            )
            
            # Layout
            button_box = widgets.HBox([accept_btn, skip_btn], 
                                     layout=widgets.Layout(gap='10px'))
            main_box = widgets.VBox([
                label,
                button_box,
                widgets.HBox([progress]),
                status_label
            ], layout=widgets.Layout(gap='10px', padding='10px'))
            
            display(main_box)
        
        # Shared state using threading Event
        accept_event = threading.Event()
        skip_event = threading.Event()
        done_event = threading.Event()
        
        def on_accept(b):
            accept_event.set()
            done_event.set()
            with output:
                accept_btn.disabled = True
                skip_btn.disabled = True
                status_label.value = "✓ Accepted!"
        
        def on_skip(b):
            skip_event.set()
            done_event.set()
            with output:
                accept_btn.disabled = True
                skip_btn.disabled = True
                status_label.value = "⏭ Skipped!"
        
        # Register callbacks
        accept_btn.on_click(on_accept)
        skip_btn.on_click(on_skip)
        
        # Background thread for progress updates
        def update_progress():
            start_time = time.time()
            while not done_event.is_set():
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    done_event.set()
                    break
                
                # Update progress in main thread
                remaining = timeout - elapsed
                progress_value = int((elapsed / timeout) * 100)
                
                with output:
                    progress.value = progress_value
                    status_label.value = f'Waiting {remaining:.1f}s...'
                
                time.sleep(0.1)
            
            # Final update
            if not accept_event.is_set() and not skip_event.is_set():
                with output:
                    progress.value = 100
                    status_label.value = "⏱ Timed out!"
                    accept_btn.disabled = True
                    skip_btn.disabled = True
        
        # Start progress thread
        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()
        
        # Wait for completion
        done_event.wait(timeout=timeout + 0.5)
        progress_thread.join(timeout=0.5)
        
        # Brief pause to show final status
        time.sleep(0.5)
        
        # Clear the output
        output.clear_output()
        
        # Return result
        if accept_event.is_set():
            print(f"✓ Mock note added: {accept_value}")
            return accept_value
        elif skip_event.is_set():
            print("⏭️  Skipped - no mock note added")
            return None
        else:
            print("⏱️  Timeout - no mock note added")
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