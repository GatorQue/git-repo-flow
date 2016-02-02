#
# Copyright (C) 2016 Ryan Lindeman
#
# Licensed under the Apache License, Version 2.0 (the "License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import os
import optparse
import sys

from command import Command
from git_command import GitCommand

class Flow(Command):
  common = True
  helpSummary = "Perform git flow commands for all flow enabled projects"
  helpUsage = """
%prog <subcommand>...

Available sub commands are:

  init                      Initialize a new git repo with support for the branching model.

  feature                   Lists all the existing feature branches in the local repository
  feature start <name>      Start new feature <name>
  feature finish <name>     Finish feature <name>
  feature publish <name>    Publish feature branch <name> on origin.
  feature track <name>      Start tracking feature <name> that is shared on origin
  feature diff <name>       Show all changes in <name> that are not in <develop>
  feature checkout <name>   Switch to feature branch <name>
  feature pull <name>       Pull feature <name> from <remote>
  feature delete <name>     Delete a given feature branch

  release                   List existing release branches in the local repository
  release start <version>   Start a new release <version>
  release finish <version>  Finish a release <version>
  release publish <version> Publish the release <version> on origin
  release track <version>   Start tracking release <version> that is shared on origin
  release delete <version>  Delete the given release <version>

  hotfix                    Lists all local hotfix branches in the local repository
  hotfix start <version>    Start a new hotfix <version>
  hotfix finish <version>   Finish a hotfix <version>
  hotfix publish <version>  Publish the hotfix <version> on origin
  hotfix delete <name>      Delete the given release <version>

Experimental sub commands: Use at own risk!

  support                         List all local support branches
  support start <version> <base>  Start a new support branch name <version> based on <base>
  
For more detailed information, refer to the 'git flow' documentation. 
"""
  helpDescription = """
'%prog' command performs the specified git flow command in each flow enabled
project.

A projects is flow enabled if it has a <flow> element definition. The flow element
definition can either be attached to the <project> element, or inherited from the 
<remote> element. 

The command is equivalent to:

  repo forall [<flow projects>...] -c git flow <subcommand>...
"""

  # Override base method so we can disable interspersed arguments and
  # allow arguments to be passed unmolested to our git flow command
  @property
  def OptionParser(self):
    if self._optparse is None:
      try:
        me = 'repo %s' % self.NAME
        usage = self.helpUsage.strip().replace('%prog', me)
      except AttributeError:
        usage = 'repo %s' % self.NAME
      self._optparse = optparse.OptionParser(usage = usage)
      self._Options(self._optparse)
      self._optparse.disable_interspersed_args()
    return self._optparse

  def Execute(self, opt, args):
    if not args:
      self.Usage()

    # first argument is the flow subcommand to perform
    cmd_name = args[0]
    flow_commands = ['init', 'feature', 'release', 'hotfix', 'support']

    # Verify the flow subcommand exists and prepare it for execution
    if not cmd_name in flow_commands:
      print("repo: '%s' is not a flow subcommand.  See 'repo help flow'." %
            cmd_name, file=sys.stderr)
      sys.exit(1)

    # Add flow before the arguments
    args.insert(0, 'flow')

    # Retrieve a list of all projects
    projects = []
    all_projects = self.GetProjects(projects,
                                    missing_ok=bool(self.gitc_manifest))

    # Find flow enabled projects
    for project in all_projects:
      if project.flow:
        projects.append(project)

        if (project.GetBranch(project.flow.branch_master) != None or \
            project.GetBranch(project.flow.branch_develo) != None) and \
           not cmd_name == 'init':
          print("error: %s/ missing develop and master branches, run repo flow init" %
                project.relpath)
          sys.exit(1)

    # Perform command on each project
    for project in projects:
      print("Project: %s/" % project.relpath)

      if cmd_name == 'init':
        project.flow.SetConfig(project.config, project.remote.name)
        project.StartBranch(project.flow.branch_master)
        project.StartBranch(project.flow.branch_develop)

      p = GitCommand(project, args, capture_stderr = True)
      if p.Wait() != 0:
        print(p.stderr, file=sys.stderr)
        sys.exit(1)

