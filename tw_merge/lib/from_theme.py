from typing import Callable, Dict, List, Any
from .types import ThemeObject, ClassGroup

def from_theme(key: str) -> Callable:
    def theme_getter(theme: Dict[str, Any]) -> List[str]:
        # Theme is passed in when the function is called
        return theme.get(key, [])
    
    # Only need to set the flag, don't store theme
    theme_getter.is_theme_getter = True
    return theme_getter