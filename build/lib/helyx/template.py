from ansible_vault import Vault
from jinja2 import Template
import yaml

class JinjaTemplate():
    def __init__(self, template_file, variable_files, vault=None):
        """
        Intializes Template class with a template file, 
        and a variable file. 
        IE:

            from template import JinjaTemplate
            data = JinjaTemplate("test.j2", "test.yaml")
            data.render_template()
        """
        self.template_file = template_file
        self.variable_files = variable_files
        self.vault = vault
        self.jinja2_data = open(self.template_file).read()
        self.variable_data = {}
        for file in self.variable_files:
            file_data = open(file).read()
            if "ANSIBLE_VAULT" in file_data:
                vault = Vault(self.vault)
                file_data = vault.load(file_data)
                self.variable_data.update(file_data)

                self.is_encrypted = True
            else:
                file_data = yaml.load(file_data,Loader=yaml.FullLoader)
                self.variable_data.update(file_data)
                self.is_encrypted = False   

    def render_template(self):
        template_data = Template(self.jinja2_data)
        self.rendered = template_data.render(self.variable_data)
        return self.rendered


