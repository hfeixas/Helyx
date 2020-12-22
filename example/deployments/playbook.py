from helyx.playbook import Playbook

Helyx = Playbook(
    "templates/ip_address.j2",
    variable_files= ["vars/all.yml"],
    target={"hosts" : ["R1"]},
    dry_run=True,
    )

Helyx.main()
