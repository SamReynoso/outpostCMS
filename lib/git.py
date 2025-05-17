import os
import sys
import subprocess
from pathlib import Path

import config
from templates.python import PUBLISH_REPOSITORY_README, WORKING_REPOSITORY_README
from lib.fsutils import mkdir, write, touch_json


def run_git_command(repo_path, *args):
    print(f"[INFO] Running git command: {' '.join(['git'] + list(args))} in {repo_path}")
    try:
        result = subprocess.run(
            ['git'] + list(args),
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()


def head(path):
    try:
        head = run_git_command(path, 'rev-parse', 'HEAD')
        return head
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to get HEAD: {e.stderr.strip()}")
        return None

def has_changes(path):
    changes = run_git_command(path, 'status', '--porcelain')
    return bool(changes)


def unique_project(path, branch):
    project_path = path  /  branch
    if os.path.exists(project_path):
        return False
    return True


def hash(path):
    return run_git_command(path, 'rev-parse', 'HEAD')

def diff(path, file):
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'diff', '-U10000', '--cached', file)

def diff_index(path, group, project):
    index =  group + '/' +  project  + '/' + 'index.html'
    print(f"[INFO] Diffing index: {index}")
    return diff(path, index)

def diff_meta(path, group, project):
    meta_file =  group + '/' +  project  + '/' + 'meta.json'
    print(f"[INFO] Diffing meta: {meta_file}")
    return diff(path, meta_file)


def status(path, group, project):
    project_dir =  group + '/' + project
    return run_git_command(
            path,
            'status',
            '--porcelain',
            )



def change_log(path, group, project):
    project_dir =  group + '/' + project
    return run_git_command(
            path,
            'log',
            '--pretty=format:"%h %ad %s"',
            '--date=iso',
            project_dir
            )


def current_branch(path):
    branch = run_git_command(path, 'rev-parse', '--abbrev-ref', 'HEAD')
    return branch


def show(path, commit_hash):
    return run_git_command(path, 'show', commit_hash)


def go_to(path, commit_hash):
    run_git_command(path, 'checkout', commit_hash)


def save(path, message):
    run_git_command(path, 'add', '.')
    run_git_command(path, 'commit', '-m', message)


def auto_save(path):
    if has_changes(path):
        save(path, "Changes saved automatically")


def submit(path, branch):
    run_git_command(path, 'merge', branch)


def new_branch(path, branch):
    if not unique_project(path, branch):
        raise Exception(f"Project {branch} already exists")
    auto_save(path)
    run_git_command(path, 'checkout', '-b', branch)


def change_branch(path, branch):
    auto_save(path)
    run_git_command(path, 'checkout', branch)


'''




Initialization
'''
def init():
    def init_repo(path):
        run_git_command(path, 'init')

    def init_worktree(path, branch_name):
        working_path = f"../{branch_name}"
        run_git_command(path, 'worktree', 'add', working_path, branch_name)

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
    save(publish_path, "Initializing Canonical Repository")
    run_git_command(publish_path, 'branch', config.WORKING)
    init_worktree(publish_path, config.WORKING)
    readme(canon / config.WORKING, WORKING_REPOSITORY_README)


if __name__ == "__main__":
    init()


