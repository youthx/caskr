import logging 
def _Verbose(level: int = logging.INFO):
    class _VerboseBase(object):
        log_level = level 
        
        def __init__(self, *args, **kwargs):
            self._logger = logging.getLogger(f"caskr.{self.__class__.__name__}")
            super().__init__(*args, **kwargs)
            
        def log(self, msg, *args, **kwargs):
            self._logger.log(self.log_level, msg, *args, **kwargs)

            
    return _VerboseBase

