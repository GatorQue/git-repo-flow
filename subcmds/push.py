#
# Copyright (C) 2016 Pieter Smith
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
import sys

from command import Command
from git_config import IsId
from git_command import git
import gitc_utils
from progress import Progress
from project import SyncBuffer

class Push(Command):
  common = True
  helpSummary = "Pushes local updates to remote branches"
  helpUsage = """
%prog [--all | <project>...]
"""
  helpDescription = """
'%prog' updates remote refs using local refs, while sending objects necessary to complete the given refs.
Projects that do not have a branch checked out are skipped.
"""

  def _Options(self, p):
    p.add_option('--all',
                 dest='all', action='store_true',
                 help='push in all projects')

  def Execute(self, opt, args):

    err = []
    projects = []
    if not opt.all:
      projects = args
      if len(projects) < 1:
        print("error: at least one project must be specified", file=sys.stderr)
        sys.exit(1)

    if self.gitc_manifest:
      all_projects = self.GetProjects(projects, manifest=self.gitc_manifest,
                                      missing_ok=True)
      for project in all_projects:
        if project.old_revision:
          project.already_synced = True
        else:
          project.already_synced = False
          project.old_revision = project.revisionExpr
        project.revisionExpr = None
      # Save the GITC manifest.
      gitc_utils.save_manifest(self.gitc_manifest)

    all_projects = self.GetProjects(projects,
                                    missing_ok=bool(self.gitc_manifest))

    pm = Progress('Pushing', len(all_projects))
    for project in all_projects:
      pm.update()

      if self.gitc_manifest:
        gitc_project = self.gitc_manifest.paths[project.relpath]
        # Pull projects that have not been opened.
        if not gitc_project.already_synced:
          proj_localdir = os.path.join(self.gitc_manifest.gitc_client_dir,
                                       project.relpath)
          project.worktree = proj_localdir
          if not os.path.exists(proj_localdir):
            os.makedirs(proj_localdir)
          project.Sync_NetworkHalf()
          sync_buf = SyncBuffer(self.manifest.manifestProject.config)
          project.Sync_LocalHalf(sync_buf)
          project.revisionId = gitc_project.old_revision

      if not project.Push():
        err.append(project)
    pm.end()

    if err:
      for p in err:
        print("error: %s/: cannot push" % p.relpath,
              file=sys.stderr)
      sys.exit(1)
