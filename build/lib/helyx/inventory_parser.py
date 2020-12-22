import yaml

class Inventory():
    def __init__(self, groups=[], hosts=[], inventory_file="inventory/inventory.yaml"):
        """
        Intializes Inventory Class and returns a list of Ips for the deployment.
        Either Groups, or Hosts can be provided. Default inventory Path Described Above.

        IE:
            inv = Inventory(
                groups=["Atlanta", "Chicago"],
                hosts=["AtlantaR1"]
            )
            inv.get_deployment_ips()

        """
        self.groups = groups
        self.hosts = hosts
        self.inventory_data = yaml.load(open(inventory_file),Loader=yaml.FullLoader)
        self.inventory_hosts = list()
        self.playbook_items = list()
    
    def get_all_hosts(self):
        try:
            for group, attributes in self.inventory_data.items():
                for item in attributes:
                    for key, value in item.items():
                        name = key
                        ip = value['host']
                        self.inventory_hosts.append({
                            "ip" : ip,
                            "name" : name,
                            "group": group
                        })
        except AttributeError:
            pass
    
    def get_host_by_ip(self, ip):
        """
        Return a single hostname from an inquiry with a single ip.
        Callback from playbook, for output to user.
        """
        self.get_all_hosts()
        for host in self.inventory_hosts:
            if host['ip'] == ip:
                host = host['name']
                
        return host
    def get_deployment_ips(self):
        """
        Get a list of ips parsed from target.
        """
        self.get_all_hosts()
        for host_name in self.hosts:
            for host in self.inventory_hosts:
                if host['name'] == host_name:
                    self.playbook_items.append(
                        host['ip']
                    )
        for group_name in self.groups:
            for host in self.inventory_hosts:
                if host['group'] == group_name:
                    self.playbook_items.append(
                        host['ip']
                    )
        self.parsed_playbook_deployments = list(set(self.playbook_items))
        
        return self.parsed_playbook_deployments