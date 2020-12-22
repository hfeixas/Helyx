from helyx.device import Device
from helyx.template import JinjaTemplate
from helyx.config_parser import Config, Colors
from helyx.inventory_parser import Inventory
from helyx.database import Database
import threading
import argparse
import getpass
import os

class Playbook():
    def __init__(self, template, variable_files, target, dry_run=True):
        """
        Class to load, and execute a playbook. This is the entrypoint for
        Helyx, any subsequent workload should be initiated from here.
        Usage:
            Helyx = Playbook(
                "templates/secrets.j2",
                variable_files= ["vars/secrets.yml", "vars/all.yaml"],
                target={"hosts" : ["R1"]},
                dry_run=True,
                )
            Helyx.main()
        """
        self.template = template
        self.variable = variable_files
        self.target = target
        self.dry_run = dry_run
        self.colors = Colors

    def load_args(self): 
        """
        Loads any arguments needed for the cli utility.
        Also loads in user SSH password to be used in the
        cli utility.
        Usage:
            helyx playbook-file.py --user username
        """
        parser = argparse.ArgumentParser(description='Helyx Coammand Line Assistant')
        parser.add_argument('--user', default="",
                            help='IOS Cli Username to Execute the playbook')
        parser.add_argument('--vault', default="",
                            help='IOS Cli Username to Execute the playbook')
        args = parser.parse_args()
        self.user = args.user
        self.vault = args.vault
        self.password = getpass.getpass("SSH Password:")

    def load_candidate_config(self):
        """
        Uses the inventory class and the Template class to load the 
        canidate config, as well as return a list of target ips.
        """
        self.inventory = Inventory(**self.target)
        self.deployments = self.inventory.get_deployment_ips()
        self.render_data = JinjaTemplate(self.template, self.variable, self.vault)
        self.candidate_config = self.render_data.render_template()

    def do_work(self, ip):
        """
        Main worker, executes our workload and adds the candidate
        configuration if needed.
        """
        connection = Device(
            ip = ip,
            credentials = {
                "username" : self.user,
                "password" : self.password
            }
        )
        running_config = connection.get_running_config()
        data = Config(running_config, self.candidate_config)
        change = data.check_for_change()
        host_name = self.inventory.get_host_by_ip(ip)
        print("""
            ██╗  ██╗███████╗██╗  ██╗   ██╗██╗  ██╗
            ██║  ██║██╔════╝██║  ╚██╗ ██╔╝╚██╗██╔╝
            ███████║█████╗  ██║   ╚████╔╝  ╚███╔╝ 
            ██╔══██║██╔══╝  ██║    ╚██╔╝   ██╔██╗ 
            ██║  ██║███████╗███████╗██║   ██╔╝ ██╗
            ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝
        """
        )
        if change:
            print("██████████████████████████████████████████████████████")
            print(self.colors.BOLD + f"        Host: {host_name}  IP: {ip}                  ")
            print("██████████████████████████████████████████████████████")        
            print(self.colors.WARNING + "Change Needed Detected:\n")
        else:
            print("██████████████████████████████████████████████████████")
            print(f"        Host: {host_name}  IP: {ip}                  ")
            print("██████████████████████████████████████████████████████")
            print(self.colors.OKGREEN + "No Change needed")

        if self.dry_run and change:
            candidate_change = data.get_config_set()
            for command in self.candidate_config.split('\n'):
                if command in candidate_change:
                    print(self.colors.WARNING + f" + {command}")
                else:
                    print(self.colors.OKBLUE + command)

        elif not self.dry_run and change:
            commands_to_be_added = []
            candidate_change = data.get_config_set()
            for command in self.candidate_config.split('\n'):
                if command in candidate_change:
                    commands_to_be_added.append(command)
            
            database = Database(host_name, commands_to_be_added)
            database.add_command()
                    
            connection.send_config(self.candidate_config.split('\n'))

    def main(self):
        """
        Main function of the PLaybook class, responsible for
        invokation of args and candidate config.
        This function runs multithreaded to assist with several target
        devices.
        """
        self.load_args()
        self.load_candidate_config()
        self.threads = list()
        for item in self.deployments:
            t = threading.Thread(target=self.do_work, args=(item,))
            t.start()
            self.threads.append(t)
        for t in self.threads:
            t.join()

