import re
import os
import yaml
import sys
from typing import List, Any


class Config(object):

    def __init__(self, filepath):

        # Load in the config file at the given filepath
        with open(filepath) as file_stream:
            self.config = yaml.safe_load(file_stream.read())

        #account setup
        self.user_id = self.get_config(["matrix", "user_id"], required=True)
        self.user_password = self.get_config(["matrix", "user_password"], required=True)
        self.homeserver_url = self.get_config(["matrix", "homeserver_url"], required=True)

        #database setup
        self.name = self.get_config(["database", "name"], required=True)
        self.user = self.get_config(["database", "user"], required=True)
        self.password = self.get_config(["database", "password"], required=True)
        self.host = self.get_config(["database", "host"], required=True)
        self.port = self.get_config(["database", "port"], required=True)


    def get_config(
            self,
            path: List[str],
            default: Any = None,
            required: bool = True,
    ) -> Any:
        """Get a config option from a path and option name, specifying whether it is
        required.
        """
        # Sift through the the config until we reach our option
        config = self.config
        for name in path:
            config = config.get(name)
        return config
