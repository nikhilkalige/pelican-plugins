import git
from pelican import signals
from pelican.utils import slugify
import logging
import os


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
        logger.warn("IUP: There are no commits, please add commit changes and run again")


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

def register():
    signals.initialized.connect(initialize)
