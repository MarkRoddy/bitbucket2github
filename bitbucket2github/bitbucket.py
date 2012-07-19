#!/usr/bin/env python

import urllib2
import json
from scriptine.shell import sh

base_url = 'https://api.bitbucket.org/1.0'

def repos(username):
    """ Returns the list of public repos owned by username """

    url = base_url + '/users/' + username + '/'
    f = urllib2.urlopen(url)
    response = json.loads(f.read())

    return [
        {
            "name":repo.get('slug'),
            "description":repo.get('description', ''),
            "homepage":repo.get('website', ''),
            "scm":repo.get("scm"),
        } for repo in response.get('repositories')
    ]



def repo_exists(reponame, username):
    """ Checks whether the repo for that user exists """
    try:
        url = base_url + '/repositories/' + username + '/' + reponame + '/'
        response = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return False
    else:
        return True


def create_repo(repo, username, password):
    """ Creates a public repository with the given credentials """

    reponame = repo['name']

    if not repo_exists(reponame, username):
        print "Creating " + reponame + " in BitBucket"
        # Somehow BitBucket authentication with urllib2 is not working. So using this ugly approach.
        cmd = 'curl -d "name={reponame}" -d "description={description}" -d "website={url}" -u {username}:{password} {base_url}/repositories/'
        cmd = cmd.format(reponame=reponame,
                         username=username,
                         password=password,
                         base_url=base_url,
                         description=repo['description'],
                         url=repo['homepage'])

        sh(cmd)
