#!/usr/bin/env python

""" This script backs up all public repos of a BitBucket user to GitHub.
"""

import tempfile
import os

import vault
from scriptine.shell import sh
import bitbucket, github

bitbucket_url = 'http://bitbucket.org/{0}/{1}'
github_url = 'git@github.com/{0}/{1}.git'
tmp_dir = tempfile.gettempdir()

def HgPullOrClone(remote_repo, local_repo):
    if os.path.exists(local_repo):
        return sh('hg pull {0} -R {1}'.format(remote_repo, local_repo))
    else:
        return sh('hg clone {0} {1}'.format(remote_repo, local_repo))

def GitPullOrClone(remote_repo, local_repo):
    if os.path.exists(local_repo):
        os.chdir(local_repo)
        cmd = 'git --git-dir="{1}/.git" --work-tree="{1}" pull {0} master'.format(remote_repo, local_repo)
        print cmd
        return sh(cmd)
    else:
        cmd = 'git clone {0} {1}'.format(remote_repo, local_repo)
    print cmd
    return sh(cmd)
    
def backup(repo, bitbucket_username, github_username, github_api_token):
    print "Syncing %s from BitBucket to GitHub" % repo['name']
    # github.create_repo(repo, github_username, github_api_token)

    bitbucket_repo = bitbucket_url.format(bitbucket_username, repo['name'])
    github_repo = github_url.format(github_username, repo['name'])
    local_repo = os.path.join(tmp_dir, repo['name'])

    if repo['scm'] == 'hg':
        # TODO GET HG+GIT WORKING
        return 0 # skipping for now
        if (0 != HgPullOrClone(bitbucket_repo, local_repo)):
            print "Error getting repo"
            return 1
        sh('hg bookmark master -f -R {0}'.format(local_repo))
        github_repo = "git+ssh://" + github_repo
        if (0 != sh('hg push {0} -R {1}'.format(github_repo, local_repo))):
            print "Error pushing changes"
            return 1
    else:
        # assume it's git
        if (0 != GitPullOrClone(bitbucket_repo, local_repo)):
            print "Error getting repo"
            return 1;
        cmd = 'git --git-dir={1}/.git --work-tree={1} push ssh://{0}'.format(github_repo, local_repo)
        print cmd
        if (0 != sh(cmd)):
            print "Error pushing changes"
            return 1
    return 0

def main():
    bitbucket_username = vault.get('bitbucket.org', 'username')
    github_username = vault.get('github.com', 'username')
    github_api_token = vault.get('github.com', github_username)
    

    for repo in bitbucket.repos(bitbucket_username):
        if (0 != backup(repo, bitbucket_username, github_username, github_api_token)):
            break


if __name__ == '__main__':
    main()
