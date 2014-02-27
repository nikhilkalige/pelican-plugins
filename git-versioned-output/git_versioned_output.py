import git
from pelican import signals
import logging
import os
import sys


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: git-versioned-output: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def initialize(pelican):
    logger.debug("Begin")
    #get current working directory
    output_path_name = pelican.settings.get("GIT_VERSIONED_OUTPUT_TAG", "v-{tag}")
    (working_path, content) = os.path.split(pelican.path)
    # check if git is initialized
    try:
        repo = git.Repo(working_path)
    except git.InvalidGitRepositoryError:
        # repo is not initialized, initialize now
        repo = git.Repo.init(working_path)
        logger.debug("Initialized new repository")
    create_gitignore()

    # if working directory is dirty ... quit plugin
    if not repo.is_dirty() and not repo.untracked_files:
        tags_list = repo.tags
        current_commit = repo.commit()
        if not tags_list:
            # there are no tags, quit now
            logger.warning("There are no tags, output will generated as usual")
            return
        if output_path_name.find("{tag}") < 1:
            logger.warning("Invalid plugin setting, output will be generated as usual")
            return
        if tags_list[-1].commit != current_commit:
            logger.warning("Current commit is not tagged, output will generated as usual")
            return

        output_path_name = output_path_name.replace("{tag}", tags_list[-1].name)
        output_path = os.path.join(pelican.output_path, output_path_name)
        if os.path.isdir(output_path) and os.listdir(output_path):
            logger.warning("Output for tag %s has already been generated, quiting pelican", tags_list[-1].name)
            sys.exit(0)
        pelican.output_path = output_path
        pelican.settings["OUTPUT_PATH"] = output_path
        logger.debug("Output will generated at %s", output_path)
    else:
        logger.warning("Repo is dirty or there are untracked files, output will be generated as usual")


def create_gitignore():
    """
        Create .gitignore file
    """
    if not os.path.exists('.gitignore'):
        open('.gitignore', 'w').close()
        logger.debug(".gitignore created")
    # add *.pyc and output to gitignore
    ignore_list = open(".gitignore").readlines()
    ouput = open(".gitignore", 'a')
    for line in ['output\n', '*.pyc\n']:
        if line not in ignore_list:
            ouput.write(line)

    logger.debug("Updated .gitignore")
    ouput.close()


def register():
    signals.initialized.connect(initialize)
