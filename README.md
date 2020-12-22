# Helyx

Helix is a Python library for for quickly delivering Jinja templated "playbooks" to cisco IOS devices, leveraging the speed of python without the bloat of ansible.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install helyx.

```bash
pip3 install https://github.com/hfeixas/Helyx.git
```

## Structure
The folder should follow a certain structure so things would work out of the box. Helyx supports a yaml based inventory with grouping.

Example structure:
```shell
.
├── deployments
│   └── playbook.py
├── inventory
│   └── inventory.yaml
├── templates
│   └── secrets.j2
└── vars
    ├── all.yml
    └── secrets.yml
```

Example inventory file:

```yaml
Site1:
  - Router1:
      host: 192.168.1.1

```

Variables are key/value pairs to be used by Jinja2 templating engine. These could be written in plain text or encrypted with ansible-vault. If encrypted the "vault" argument should be passed to the cli runner.

Example vars file:

```yaml
interfaces:
  - ip: 192.168.1.1
    mask: 255.255.255.0
    interface: loopback0
```

## Usage

Create a python playbook file and define the target hosts or groups, target variable files, specify whether the execution is a dry run or not.

Deployment on a single host without utilizing a variable file.
```python
from helyx.playbook import Playbook

Helyx = Playbook(
    "templates/ip_addresses.j2",
    variable_files= [],
    target={"hosts" : ["Router1"]}, 
    dry_run=True,
    )

Helyx.main()

```

Then Simple execute the playbook via the cli tool:
```shell
# helyx playbook.py --user "my_user"
```


Deployment on groups and hosts with a variable file.

```python
from helyx.playbook import Playbook

Helyx = Playbook(
    "templates/secrets.j2",
    variable_files= ["vars/secrets.yml", "vars/users.yml"],
    target={"groups" : ["Site1"], "hosts" : ["Router2"]}, 
    dry_run=True,
    )

Helyx.main()

```

Then Simple execute the playbook via the cli tool:
```shell
# helyx playbook.py --user "my_user" --vault "my_ansible_vault_secret"
```

Sample output from dry run:
```shell
SSH Password:

            ██╗  ██╗███████╗██╗  ██╗   ██╗██╗  ██╗
            ██║  ██║██╔════╝██║  ╚██╗ ██╔╝╚██╗██╔╝
            ███████║█████╗  ██║   ╚████╔╝  ╚███╔╝ 
            ██╔══██║██╔══╝  ██║    ╚██╔╝   ██╔██╗ 
            ██║  ██║███████╗███████╗██║   ██╔╝ ██╗
            ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝
        
██████████████████████████████████████████████████████
        Host: R1  IP: 192.168.1.1                  
██████████████████████████████████████████████████████
Change Needed Detected:


 + interface loopback0 
 +   description 
 +   ip address 192.168.1.1 mask 255.255.255.0
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
