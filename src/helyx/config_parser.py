
class Config():
    def __init__(self, running_config, parsed_config):
        self.running_config = running_config
        self.parsed_config = parsed_config
        self.change_needed = False
        self.config_set = []

    def compare_config(self):
        """
        This function will check a running configuration
        for a change needed in the destination file.
        IE:
            from config_parser import Config
            data = Config (old_config, new_config)
            data.compare_config()
        """
        for line in self.parsed_config.splitlines():
            if line in self.running_config:
                pass
            else:
                print(f"+ {line}")
                
    def check_for_change(self):
        """
        This function will return a boolean value for whether
        an execution of a template requires a change. 
        IE:
            from config_parser import Config
            data = Config(old_config, new_config)
            data.check_for_change()

        """
        for line in self.parsed_config.splitlines():
            if line in self.running_config:
                pass
            else:
                self.change_needed = True
                self.config_set.append(line)
        
        return self.change_needed

    def get_config_set(self):
        self.check_for_change()

        return self.config_set

class Colors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'