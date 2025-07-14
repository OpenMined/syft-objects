# Simple prompt implementation that actually works in Jupyter

import time
from typing import Optional


def prompt_with_timeout(
    message: str, 
    timeout: float = 2.0, 
    jupyter_compatible: bool = True,
    accept_value: Optional[str] = None
) -> Optional[str]:
    """
    Simplified prompt that works reliably.
    
    For Jupyter: Shows message and waits for timeout.
    User can set config.mock_note_sensitivity = "always" to auto-accept.
    """
    if accept_value is None:
        accept_value = message
    
    print(f"\n📊 {message}")
    print(f"⏱️  Auto-accepting in {timeout}s...")
    print("💡 Tip: Set config.mock_note_sensitivity = 'always' to auto-accept all suggestions")
    
    # Simple sleep-based timeout
    time.sleep(timeout)
    
    # Auto-accept after timeout for better UX
    print(f"✓ Mock note added: {accept_value}")
    return accept_value