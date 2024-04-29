from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: extract_git_path
    author: diademiemi (@diademiemi)
    version_added: "6.0.0"
    short_description: This filter is designed to return the path of the Git repository, omitting the host
    description:
        - This filter is designed to return the path of the Git repository, omitting the host
    options:
        omit_dot_git:
            description:
            - Omit the .git from the path
            type: bool
            required: False
            default: False
"""


from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

import re

def _extract_git_path(*args, **kwargs):
    aav = AnsibleArgSpecValidator(data=kwargs, schema=DOCUMENTATION, name="extract_git_path")
    valid, errors, updated_data = aav.validate()

    if not valid:
        raise AnsibleFilterError(errors)

    if args:
        value = args[0]
    else:
        raise AnsibleFilterError("value must be a string")
    
    if value is None:
        raise AnsibleFilterError("value must be a string")
    
    if not isinstance(value, str):
        raise AnsibleFilterError("value must be a string")

    if value.endswith(".git") and updated_data.get("omit_dot_git", True):
        value = value[:-4]

    if value.startswith("http://") or value.startswith("https://"):
        return re.sub(r".*://[^/]*/", "", value)
    elif '@' in value:
        return re.sub(r".*@[^:]*:", "", value)
    else:
        raise AnsibleFilterError("Invalid Git remote endpoint")

class FilterModule(object):
    """path filters"""

    def filters(self):
        return {"extract_git_path": _extract_git_path}