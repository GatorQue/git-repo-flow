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

from subcmds import sync

class Pull(sync.Sync):
  common = True
  helpSummary = "Update working tree to the latest revision (branches are checked out or merged)"
  helpUsage = """
%prog [<project>...]
"""
  helpDescription = """
The '%prog' command is similar to the 'repo sync' command, but branches are
checked out and merged if the project 'revision' specifies a branch. 
   
""" + sync.Sync.helpDescription.replace("rebase any new local changes\non top of", "merge any new local changes with")

  def __init__(self):
    super(Pull,self).__init__(mergeDontRebase=True,
                              checkoutBranches=True)
