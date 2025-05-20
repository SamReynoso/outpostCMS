from pathlib import Path

from lib import git
from lib.fsutils import mkdir, write, touch_json, cp
from outpost_d import config


def init():
    def init_repo(path):
        """
        Initialize a new git repository in the given path.
        """
        git.run_git_command(path, 'init')

    def init_worktree(path, branch_name):
        """
        Create a new branch and add a worktree for it.
        """
        git.run_git_command(path, 'branch', config.WORKING)
        working_path = f"../{branch_name}"
        git.run_git_command(path, 'worktree', 'add', working_path, branch_name)

    def ignore(path):
        """
        Create a .gitignore file in the canonical directory.
        """
        content = '''# Git Ignore\nREADME.md'''
        file_path = path / '.gitignore'
        write(file_path, content)

    def site_map():
        """
        Create a 'site map' file in the canonical directory.
        """
        touch_json(canon, config.SITE_MAP, {})

    def readme(src: Path, dst: Path, name: str = "README.md"):
        """
        Copy the README file from the source to the destination.
        """
        cp(src, dst / name, r=True)


    canon = Path(config.CANON)
    publish_path = canon / config.PUBLISH

    # Check if the canonical directory already exists
    if not config.DEBUG and not config.CACHE_DELAY:
        raise FileExistsError(f"Directory {canon} already exists.")

    # Create the canonical directory and its subdirectories
    mkdir(canon)
    site_map()
    mkdir(publish_path)

    # Create the publish repository and add the README file
    init_repo(publish_path)
    ignore(publish_path)
    readme(Path(config.PUBLISH_README), publish_path)
    git.commit(publish_path, "Initializing Canonical Repository")

    # Create the 'working' directory and worktree
    init_worktree(publish_path, config.WORKING)
    readme(Path(config.WORKING_README), publish_path)


if __name__ == "__main__":
    init()


