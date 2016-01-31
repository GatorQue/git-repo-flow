#
# Copyright (C) 2016 Ryan Lindeman
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
%prog <flow command> [<flow command arguments>...]
"""
  helpDescription = """
'%prog' command performs the specified git flow command in each flow enabled
(which has a <flow> elements in either the project or remote) project.

The command is equivalent to:

  repo forall [<flow projects>...] -c git flow <command> <arguments>
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
    flow_commands = ['help', 'feature', 'release', 'hotfix']

    # Verify the flow subcommand exists and prepare it for execution
    if not cmd_name in flow_commands:
      print("repo: '%s' is not a flow subcommand.  See 'repo flow help'." %
            cmd_name, file=sys.stderr)
      sys.exit(1)

    # Run gitflow help command if command provided is help
    if cmd_name == 'help':
      self.help()
      return

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

    # Perform command on each project
    for project in projects:
      print("Project: %s/" % project.relpath)
      p = GitCommand(project, args,
                     capture_stderr = True)
      if p.Wait() != 0:
        print(p.stderr, file=sys.stderr)
        sys.exit(1)

  def help(self):
    print("Available repo flow subcommands are:")
    print("  feature    Manage your feature branches.")
    print("    (none)   Obtain a list of feature branches")
    print("    start    Start a new feature")
    print("    finish   Finish a feature")
    print("    publish  Publish a feature")
    print("    track    Track a published feature")
    print("    diff     Show feature differences")
    print("    checkout Checkout feature")
    print("    pull     Pull updates")
    print("    delete   Delete feature branch")
    print("  release   Manage your release branches.")
    print("    (none)   Obtain a list of release branches")
    print("    start    Start a new release")
    print("    finish   Finish a release")
    print("    publish  Publish a release")
    print("    track    Track a published release")
    print("    delete   Delete release branch")
    print("  hotfix    Manage your hotfix branches.")
    print("    (none)   Obtain a list of hotfix branches")
    print("    start    Start a new hotfix")
    print("    finish   Finish a hotfix")
    print("    publish  Publish a hotfix")
    print("    delete   Delete hotfix branch")

