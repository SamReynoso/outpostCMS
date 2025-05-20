from pathlib import Path

from lib import git
from lib.fsutils import mkdir, write, touch_json, cp
from outpost_d import config


def init():
    canon = Path(config.CANON)
    publish_path = canon / config.PUBLISH
    working_path = config.WORKING

    def ignore(path):
        """ Create a .gitignore file in the canonical directory. """
        content = '''# Git Ignore\nREADME.md'''
        file_path = path / '.gitignore'
        write(file_path, content)

    def site_map():
        """ Create a 'site map' file in the canonical directory. """
        touch_json(canon, config.SITE_MAP, {})

    def readme(src: Path, dst: Path, name: str = "README.md"):
        """ Copy the README file from the source to the destination. """
        cp(src, dst / name, r=True)

    def setup():
        """ Create the canonical directory and its subdirectories. """
        if canon.exists():
            raise FileExistsError(f"Directory {canon} already exists.")
        mkdir(canon)
        site_map()
        mkdir(publish_path)

    def init_repo():
        """ Initialize a new git repository in the given path. """
        git.run_git_command(publish_path, 'init')
        ignore(publish_path)
        readme(Path(config.PUBLISH_README), publish_path)
        git.commit(publish_path, "Initializing Canonical Repository")

    def init_worktree():
        """ Create a new branch and add a worktree for it. """
        git.run_git_command(publish_path, 'branch', config.WORKING)
        tree_path = f"../{working_path}"
        git.run_git_command(publish_path, 'worktree', 'add', tree_path, config.WORKING)
        readme(Path(config.WORKING_README), publish_path)

    setup()
    init_repo()
    init_worktree()


if __name__ == "__main__":
    init()


