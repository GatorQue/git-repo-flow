# Repo Flow

Repo Flow enhances the [Google Repo project](https://code.google.com/p/git-repo/) with a [git-flow](https://github.com/nvie/gitflow) branching model.

The [git-flow](https://github.com/nvie/gitflow) branching model is applied at the manifest / composition as well as the Git project level. You can use this with any Git server, without the need for a [Gerrit Code Review](https://www.gerritcodereview.com/) server; Gerrit is a practical requirement to effectively use the [Google Repo tools](https://code.google.com/p/git-repo/).

## Background

Repo is a tool built on top of Git. It helps compose a number of Git projects into a single workspace, nicely solving repeatability issues. It was written to automate the Android Gerrit-centric development workflow. Repo however is of more generic value, which is why we created the Repo Flow enhancement. In absence of Gerrit, Repo can be used to compose a workspace from multiple Git repositories. Repo however lacks automation to update manifest files and support a git-flow branching model.

Repo Flow therefore:

1. Provides the git-flow operations at the composition and project level: 
   * ```init```: Initialize the Repo project to support git-flow the branching model.
   * ```feature```: Manage your feature branches.
   * ```release```: Manage your release branches.
   * ```hotfix```: Manage your hotfix branches.
   * ```support```: Manage your support branches.
1. Generates and merges manifests so that you can checkout and work on your feature, release, hotfix and support compositions.
1. Generates release manifests for your tagged releases.
