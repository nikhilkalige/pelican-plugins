import git
from pelican import signals
import logging
import os
import sys


logger = logging.getLogger(__name__)

_incremental_update = True

def initialize(pelican):
    global _incremental_update, _diff
    logger.debug("IUP: Begin")

    # check whether output folder has generated content
    # get output folder from settings
    ouput_location = pelican.settings.get("OUTPUT_PATH")
    if not os.path.isdir(ouput_location) or os.listdir(ouput_location) == []:
        _incremental_update = False

    if _incremental_update is False:
        logger.debug("IUP: Output path does not exist, IUP plugin disabled")

    if _incremental_update is True:
        # check if git is initialized
        try:
            repo = git.Repo("/home/nikhil/workspace/web_development/python/pelican/incremental-test")
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
        # home pc
        last_commit = "18269fb124c1f9e96ec1f6246ee184f2e195886c"
        last_commit = "f9d8519c10591a7aeff588b95ae42ee3b7ba9ab3"
        # office pc
        last_commit = "09e8fe4853862394a13be5a82e9944343e5cd93b"  # 3rd commit
        last_commit = "f42e9e4a0cefb6b7c2e6c4a4a7bfad93cd435adc"  # 2nd commit
        last_commit = "6d39c31f03b8995ade57fe9d9d5474ce6d3f5d84"  # 1st commit
        # get the diff between the commits
        _diff = current_commit.diff(last_commit)
        # check if there are any changes in config files
        if _diff:
            for x in _diff:
                if x.a_blob.name in ["pelicanconf.py", "publishconf.py"]:
                    # config files have changed, regenerate content
                    _incremental_update = False
                    break
        else:
            # there are no changes between commits, time to exit pelican
            logger.debug("IUP: There are no changes, exiting pelican")

        if _incremental_update is False:
            logger.debug("IUP: Config files have changed, regenerate whole content")


def aritcles_update(generator):
    global _incremental_update, _diff
    print("UPDATE")
    # skip if config has been changed or if output dir has been cleaned
    if _incremental_update is True:
        logger.debug("IUP: Begin working on articles")


def pages_update(generator):
    global _incremental_update, _diff
    # skip if config has been changed or if output dir has been cleaned
    if _incremental_update is True:
        logger.debug("IUP: Begin working on pages")


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


def contex(a, metadata):
    print("PREREAD")


def pre(a):
    print("CIONTEXT")


def initt(a):
    print("INIT")


def register():
    signals.initialized.connect(initialize)
    signals.article_generator_finalized.connect(aritcles_update)
    signals.page_generator_finalized.connect(pages_update)
    signals.article_generator_preread.connect(pre)
    signals.article_generator_context.connect(contex)
    signals.article_generator_init.connect(initt)
