from dataclasses import dataclass
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class VMInfo:
    ip: str
    user: str


@dataclass
class EnvInfo:
    vm: VMInfo


@dataclass
class InventoryInfo:
    dev: EnvInfo
    prod: EnvInfo


class AnsibleInventoryRenderer:
    """Class to render Ansible inventory in JSON format."""

    INDENT = 2

    def __init__(self, inventory: dict) -> None:
        self.inventory = inventory

    def list(self) -> None:
        print(json.dumps(self.inventory, indent=self.INDENT))

    def host(self, hostname: str) -> None:
        host_vars = self.inventory["_meta"]["hostvars"].get(hostname)
        if host_vars:
            print(json.dumps(host_vars, indent=self.INDENT))
            return
        print("{}")  # Host not found


class AnsibleInventoryBuilder:
    """Class to build Ansible inventory from jinja template and data."""

    def __init__(self, template_dir: Path, template_name: str) -> None:
        env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["json"]),
        )
        self.template = env.get_template(template_name)

    def build(self, inventory: InventoryInfo) -> AnsibleInventoryRenderer:
        rendered = self.template.render(inventory=inventory)
        return AnsibleInventoryRenderer(json.loads(rendered))
