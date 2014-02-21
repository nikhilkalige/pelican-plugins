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


def commit_changes():
    """
        Commit changes in the directory
    """


def register():
    signals.initialized.connect(initialize)
