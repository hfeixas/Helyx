import json
import os

class Database():
    def __init__(self, host, commands_added=[], database="database.json"):
        self.host = host
        self.commands_added = commands_added
        self.database = database

    def add_command(self):
        self.load_database()
        host_exists = False
        while not host_exists:
            for host in self.database_data["Hosts"]:
                hostname = host["name"]
                db_commands = host["commands"]
                if self.host == hostname:
                    for command in self.commands_added:
                        if command in db_commands:
                            pass
                        else:
                            db_commands.append(command)
                    host_exists = True

            if not host_exists:
                self.database_data["Hosts"].append(
                    {
                        "name" : self.host,
                        "commands" : self.commands_added
                    }
                )
                host_exists = True

        self.close_database()
                        
    def close_database(self):
        database_file = open(self.database, 'w')
        database_file.write(json.dumps(self.database_data))
        database_file.close()

    def load_database(self):
        if os.path.exists(self.database):
            self.database_data = json.loads(open(self.database).read())
        else:
            print(f"Did not find Database File. Creating: {self.database}")
            database_file = open(self.database, 'w')
            database_file.write('{"Hosts" : [{"name" : "host", "commands" : []}]}')
            database_file.close()
            self.database_data = json.loads(open(self.database).read())
