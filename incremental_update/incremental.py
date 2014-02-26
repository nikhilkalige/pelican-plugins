import git
from pelican import signals
import logging
import os
import sys


logger = logging.getLogger(__name__)


def initialize(pelican):
    logger.debug("IUP: Begin")

    # check if git is initialized
    try:
        repo = git.Repo("/home/lonewolf/workspace/web_development/python/pelican/incremental_update")
    except git.InvalidGitRepositoryError:
        # repo is not initialized, initialize now
        repo = git.Repo.init(".")
        logger.debug("IUP: Initialize new repository")
    create_gitignore()
    if not commits_present(repo):
        # there are no commits, quit now
        logger.critical("IUP: There are no commits, please add commit changes and run again")
        logger.critical("IUP: Exiting now")
        sys.exit()
    # get the current commit
    tags_list = repo.tags
    if not tags_list[0]:
        # there are no tags, quit now
        logger.critical("IUP: There are no tags, please add tags and run again")
        logger.critical("IUP: Exiting now")
        sys.exit()

    pelican.output_path = pelican.settings.get("OUTPUT_PATH") + '/' + tags_list[-1].name
    pelican.settings["OUTPUT_PATH"] = pelican.settings.get("OUTPUT_PATH") + '/' + tags_list[-1].name
    print (pelican.settings.get("OUTPUT_PATH"))
    logger.debug("IUP: Output will generated at ..")


def create_gitignore():
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
