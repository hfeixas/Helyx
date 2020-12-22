from netmiko import ConnectHandler

class Device():
    def __init__(self, ip, credentials):
        """
        Initialize this class with an ip address and a dictionaty of 
        username, pw and ip address.
        IE:
            from device import Device
            
            connection = Device(
                ip = "192.168.1.1",
                credentials = {
                    "username" : "user",
                    "password" : "pass"
                }
            )
        """
        self.ip = ip
        self.credentials = credentials
        self.session = ConnectHandler(device_type="cisco_ios", ip=self.ip,  **self.credentials)
    
    def get_running_config(self):
        """
        This function will return a string of a devices
        current running configuration.
        """
        
        output = self.session.send_command("show running-config")
        self.running_config = output

        return self.running_config

    def send_config(self, config_set):
        commands = self.session.send_config_set(config_set)
        print (commands)