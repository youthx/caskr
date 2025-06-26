import os
from typing import Any, Optional    

def get(key: str, default: Optional[Any] = None) -> Optional[str]:
    """
    Get environment variable as a string.
    Returns default if not set.
    """
    return os.environ.get(key, default)


def get_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """
    Get environment variable as int.
    Returns default if not set or invalid int.
    """
    val = os.environ.get(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


def get_bool(key: str, default: Optional[bool] = None) -> Optional[bool]:
    """
    Get environment variable as bool.
    Accepts '1', 'true', 'yes', 'on' (case-insensitive) as True.
    Returns default if not set or unrecognized.
    """
    val = os.environ.get(key)
    if val is None:
        return default
    val_lower = val.lower()
    if val_lower in ("1", "true", "yes", "on"):
        return True
    if val_lower in ("0", "false", "no", "off"):
        return False
    return default


def get_float(key: str, default: Optional[float] = None) -> Optional[float]:
    """
    Get environment variable as float.
    Returns default if not set or invalid float.
    """
    val = os.environ.get(key)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def set(key: str, value: Any) -> None:
    """
    Set an environment variable (in current process only).
    """
    os.environ[str(key)] = str(value)


def load_dotenv(dotenv_path: str = ".env") -> None:
    """
    Load environment variables from a .env file.
    Simple parser: lines with KEY=VALUE ignoring comments and blanks.
    """
    if not os.path.exists(dotenv_path):
        return

    with open(dotenv_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key not in os.environ:
                os.environ[key] = val
