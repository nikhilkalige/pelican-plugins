import git
from pelican import signals
from pelican.utils import slugify
import logging
import os
import sys


logger = logging.getLogger(__name__)


def initialize(pelican):
    logger.debug("IUP: Begin")
    # check if git is initialized
    try:
        repo = git.Repo("")
    except git.InvalidGitRepositoryError:
        # repo is not initialized, initialize now
        repo = git.Repo.init(".")
        logger.debug("IUP: Initialize new repository")
    create_ignore()
    if not commits_present(repo):
        # there are no commits, quit now
        logger.critical("IUP: There are no commits, please add commit changes and run again")
        logger.critical("IUP: Exiting now")
        sys.exit()
    # get the current commit
    current_commit = repo.commit
    # get the last commit based on which the content was generated
    # temporarily we will use hardcoded data
    last_commit = "592edb8c18de4c8c791ae548021b2321eff4dd5c"




def create_ignore():
    """
        Create .gitignore file
    """
    if not os.path.exists('.gitignore'):
        open('.gitignore', 'w').close()
        logger.debug("IUP: .gitignore created")
    # add *.pyc and output to gitignore
    ignore_list = open(".gitignore").readlines()
    ouput = open(".gitignore", 'a')
    for line in ['output\n', '*.pyc\n']:
        if line not in ignore_list:
            ouput.write(line)

    logger.debug("IUP: Updated .gitignore")
    ouput.close()


def commits_present(repo):
    """
        Commit changes in the directory
    """
    # check if there are any commits
    try:
        repo.commit()
    except ValueError:
        return False
    return True


def get_changes(repo, current_commit, last_commit):
    """
        Find files that have changed since last time content was generated
    """

def register():
    signals.initialized.connect(initialize)
