import os 
import logging

# The class `CaskrGlobalConf` contains attributes for default log level, version, and route directory,
# with a method to set the route base directory.
class CaskrGlobalConf:
    DEFAULT_LOG_LEVEL = logging.INFO
    
    __version__ = os.environ.get("caskr_version", "0.1.0")
    
    route_dir = None 


    @classmethod 
    def set_route_base_directory(cls, route_dir) -> None:
        """
        The function `set_route_base_directory` sets the route directory for a class.
        
        @param route_dir The `route_dir` parameter in the `set_route_base_directory` method is the
        directory path where the routes are located or where the base directory for routes should be
        set. This parameter allows you to specify the directory where the routes for your application
        are defined.
        """
        cls.route_dir = route_dir
        