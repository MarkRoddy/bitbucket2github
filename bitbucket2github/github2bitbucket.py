#!/usr/bin/env python

""" This script backs up all public repos of a GitHub user to BitBucket.
"""

import tempfile
import os

import vault
from scriptine.shell import sh
import bitbucket, github

github_username = vault.get('github.com', 'username')
bitbucket_username = vault.get('bitbucket.org', 'username')
bitbucket_password = vault.get('bitbucket.org', bitbucket_username)

bitbucket_url = 'ssh://hg@bitbucket.org/{0}/{1}'
github_url = 'git+ssh://git@github.com/{0}/{1}.git'
tmp_dir = tempfile.gettempdir()


def backup(repo):
    print "Syncing %s from GitHub to BitBucket" % repo['name']
    bitbucket.create_repo(repo, bitbucket_username, bitbucket_password)

    bitbucket_repo = bitbucket_url.format(bitbucket_username, repo['name'])
    github_repo = github_url.format(github_username, repo['name'])
    local_repo = os.path.join(tmp_dir, repo['name'])

    if os.path.exists(local_repo):
        sh('hg fetch {0} -R {1}'.format(github_repo, local_repo))
    else:
        sh('hg clone {0} {1}'.format(github_repo, local_repo))

    sh('hg bookmark master -f -R {0}'.format(local_repo))
    sh('hg push {0} -R {1}'.format(bitbucket_repo, local_repo))


def main():
    for repo in github.repos(github_username):
        backup(repo)


if __name__ == '__main__':
    main()
