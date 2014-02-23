import git
from pelican import signals
from pelican.utils import slugify
import logging
import os
import sys


logger = logging.getLogger(__name__)

_incremental_update = False


def initialize(pelican):
    global _incremental_update
    logger.debug("IUP: Begin")
    # check if git is initialized
    try:
        repo = git.Repo("")
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
    current_commit = repo.commit()
    # get the last commit based on which the content was generated
    # temporarily we will use hardcoded data
    last_commit = "f9d8519c10591a7aeff588b95ae42ee3b7ba9ab3"
    # get the diff between the commits
    diff = current_commit.diff(last_commit)
    # check if there are any changes in config files
    for x in diff:
        if x.a_blob.name not in ["pelicanconf.py", "publishconf.py"]:
            _incremental_update = True

    if _incremental_update is False:
        logger.debug("IUP: Config files have changed, regenerate whole content")


def aritcles_update(generator):
    global _incremental_update
    # skip if config has been changed or if output dir has been cleaned
    if _incremental_update is True:
        logger.debug("IUP: Checking articles for changes")


def pages_update(generator):
    global _incremental_update
    # skip if config has been changed or if output dir has been cleaned
    if _incremental_update is True:
        logger.debug("IUP: Checking pages for changes")


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


def get_changes(repo, current_commit, last_commit):
    """
        Find files that have changed since last time content was generated
    """


def register():
    signals.initialized.connect(initialize)
    signals.article_generator_finalized.connect(aritcles_update)
    signals.page_generator_finalized.connect(pages_update)
