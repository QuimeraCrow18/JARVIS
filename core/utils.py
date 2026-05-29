from core.logger import JarvisLogger
from core.error_manager import ErrorManager

def safe_method(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            JarvisLogger().error(f"Error en {func.__name__}: {e}")
            ErrorManager().handle_error(e, func.__name__)
            return None
    return wrapper