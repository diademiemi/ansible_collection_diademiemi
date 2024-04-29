from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: get_file_path
    author: diademiemi (@diademiemi)
    version_added: "6.0.0"
    short_description: This filter is designed to return the path of a file relative to a Git repository
    description:
        - This filter is designed to return the path of a file relative to a Git repository
"""


from ansible.errors import AnsibleFilterError

import subprocess
import os

def _get_relative_git_file(*args, **kwargs):
    if args:
        value = args[0]
    else:
        raise AnsibleFilterError("value must be a string")
    
    if value is None:
        raise AnsibleFilterError("value must be a string")
    
    if not isinstance(value, str):
        raise AnsibleFilterError("value must be a string")


    def get_git_root_path():
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()

    git_root = get_git_root_path()
    return os.path.relpath(value, git_root)


class FilterModule(object):
    """path filters"""

    def filters(self):
        return {"get_relative_git_file": _get_relative_git_file}