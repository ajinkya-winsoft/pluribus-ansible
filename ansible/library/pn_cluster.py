#!/usr/bin/python
# Test PN CLI cluster-create/cluster-delete


DOCUMENTATION = """
---
module: pn_cluster
author: "Pluribus Networks"
short_description: CLI command to create/delete a cluster
description:
  - Execute cluster-create or cluster-delete command. 
  - Requires cluster name:
  	- Alphanumeric characters
  	- Special characters like: _ 
  - Requires 2 nodes, cluster-node-1 and cluster-node-2
options:
  pn_clustercommand:
    description:
      - The C(pn_clustercommand) takes the cluster-create/cluster-delete command as value.
    required: true
    choices: cluster-create, cluster-delete
    type: str
  pn_clustername:
    description:
      - The C(pn_clustername) takes a valid name for cluster configuration.
    required: true
    type: str
  pn_clusternode1:
    description:
      - name for cluster-node 1
    required_if: cluster-create 
    type: str
  pn_clusternode2:
    description:
      - name for cluster-node 2
    required_if: cluster-create
    type: str
  pn_clustervalidate:
    description:
      - validate the cluster link
    required: false
    choices: validate, no-validate
    type: str
  pn_quiet:
    description:
      - The C(pn_quiet) option to enable or disable the system bootup message
    required: false
    type: bool
    default: true
"""

EXAMPLES = """
- name: create spine cluster 
  pn_cluster: pn_clustercommand='cluster-create' pn_clustername='spine-cluster' pn_clusternode1='spine01' pn_clusternode2='spine02' pn_clustervalidate=True pn_quiet=True
- name: delete spine cluster 
  pn_cluster: pn_clustercommand='cluster-delete' pn_clustername='spine-cluster' pn_quiet=True
"""

RETURN = """
clustercmd:
  description: the CLI command run on the target node(s).
stdout:
  description: the set of responses from the cluster command.
  returned: always
  type: list
stdout_lines:
  description: the value of stdout split into a list.
  returned: always
  type: list
stderr:
  description: the set of error responses from the cluster command.
  returned: on error
  type: list
"""
import subprocess
import shlex
import json


def main():
        module = AnsibleModule(
                argument_spec = dict(
                        pn_clustercommand = dict(required=True, type='str', choices=['cluster-create', 'cluster-delete']),
                        pn_clustername = dict(required=True, type='str'),
                        pn_clusternode1 = dict(type='str'),
                        pn_clusternode2 = dict(type='str'),
                        pn_clustervalidate = dict(required=False, type='str', choices=['validate', 'no-validate']),
                        pn_quiet = dict(default=True, type='bool')
                        ),
                required_if = (
                        [ "pn_clustercommand", "cluster-create", ["pn_clustername", "pn_clusternode1", "pn_clusternode2" ] ],
                        [ "pn_clustercommand", "cluster-delete", ["pn_clustername"] ]
                        )
        )

        clustercommand = module.params['pn_clustercommand']
        clustername = module.params['pn_clustername']
        clusternode1 = module.params['pn_clusternode1']
        clusternode2 = module.params['pn_clusternode2']
        clustervalidate = module.params['pn_clustervalidate']
        quiet = module.params['pn_quiet']

        if quiet==True:
                cli  = "/usr/bin/cli --quiet "
        else:
                cli = "/usr/bin/cli "


        if clustername:
                cluster = cli + clustercommand + ' name ' + clustername

        if clusternode1:
                cluster += ' cluster-node-1 ' + clusternode1

        if clusternode2:
                cluster += ' cluster-node-2 ' + clusternode2

        if clustervalidate:
                cluster += " " + clustervalidate

        clustercmd = shlex.split(cluster)

        p = subprocess.Popen(clustercmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        out,err = p.communicate();


        module.exit_json(
                clustercmd = cluster,
                stdout = out.rstrip("\r\n"),
                stderr = err.rstrip("\r\n"),
                changed = True
        )

from ansible.module_utils.basic import *

if __name__ == '__main__':
        main()
