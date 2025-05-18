from lib import git
from lib.fsutils import mkdir, write, touch_json
from outpost_d import config


def init():
    def init_repo(path):
        git.run_git_command(path, 'init')

    def init_worktree(path, branch_name):
        working_path = f"../{branch_name}"
        git.run_git_command(path, 'worktree', 'add', working_path, branch_name)

    def ignore(path):
        content = '''# Git Ignore\nREADME.md'''
        file_path = path / '.gitignore'
        write(file_path, content)

    def site_map():
        touch_json(canon, config.SITE_MAP, [])

    def readme(path, content):
        file_path = Path(path) / 'README.md'
        write(file_path, content)


    canon = Path(config.CANON)
    publish_path = canon / config.PUBLISH

    mkdir(config.CANON)
    site_map()
    mkdir(publish_path)
    init_repo(publish_path)

    ignore(publish_path)
    readme(publish_path, PUBLISH_REPOSITORY_README)
    git.commit(publish_path, "Initializing Canonical Repository")
    git.run_git_command(publish_path, 'branch', config.WORKING)
    init_worktree(publish_path, config.WORKING)
    readme(canon / config.WORKING, WORKING_REPOSITORY_README)


if __name__ == "__main__":
    init()


