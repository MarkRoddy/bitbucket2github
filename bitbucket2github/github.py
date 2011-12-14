#!/usr/bin/env python

from github2.client import Github

def repos(username):
    """ Returns the list of public repos owned by user """

    github = Github()
    return [{
            "name":repo.name,
            "description":repo.description or '',
            "homepage":repo.homepage or ''
        }
        for repo in github.repos.list(username)]


def repo_exists(reponame, username):
    """ Checks whether the repo for that user already exists """

    github = Github()
    try:
        repo = github.repos.show(username + '/' + reponame)
    except RuntimeError:
        return False
    else:
        return True


def create_repo(repo, username, api_token):
    """ Creates a public repository with the given credentials """

    reponame = repo['name']
    github = Github(username=username, api_token=api_token)

    if not repo_exists(reponame, username):
        print "Creating " + reponame + " in GitHub"
        github.repos.create(reponame, 
                        description=repo['description'], 
                        homepage=repo['homepage'])

