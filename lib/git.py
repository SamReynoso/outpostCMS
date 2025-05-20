import subprocess
from pathlib import Path


def run_git_command(path: Path, *args) -> tuple[str, bool]:
    print("[INFO   ] Running git command: {' '.join(['git'] + list(args))} in {path}")
    try:
        result = subprocess.run(
            ['git'] + list(args),
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"[SUCCESS] Command executed successfully")
        return result.stdout.strip(), True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR  ] Git command failed: {e.stderr.strip()}")
        return e.stderr.strip(), False


def branch(path: Path, branch: str) -> tuple[str, bool]:
    """ Create a new branch and switch to it """
    commit(path, "Creating branch")
    run_git_command(path, 'checkout', '-b', branch)
    return head(path)


def branch_name(path: Path) -> tuple[str, bool]:
    """ Get the current branch name """
    return run_git_command(path, 'rev-parse', '--abbrev-ref', 'HEAD')


def head(path: Path) -> tuple[str, bool]:
    """ Get the current commit hash """
    return run_git_command(path, 'rev-parse', 'HEAD')


def add(path: Path) -> tuple[str, bool]:
    """ Add all changes to the staging area """
    return run_git_command(path, 'add', '.')


def log(path: Path, branch: str) -> tuple[str, bool]:
    """ Get the commit hashes that in this branch """
    return run_git_command(
            path,
            'log',
            '--oneline',
            '--',
            branch,
            )

def checkout(path: Path, branch: str) -> tuple[str, bool]:
    """ Switch to an existing branch """
    commit(path, "Switching branches")
    return run_git_command(path, 'checkout', branch)


def status(path: Path) -> tuple[str, bool]:
    """ Get the status of the repository """
    return run_git_command(
            path,
            'status',
            '--porcelain',
            )

def commit(path: Path, message: str="Changes saved automatically") -> tuple[str, bool]:
    """ Commit changes to the repository """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'commit', '-m', message)


def merge(path: Path, branch: str, message: str="Merging changes") -> tuple[str, bool]:
    """ Merge changes from another branch """
    commit(path, message)
    return run_git_command(path, 'merge', branch)


def show(path: Path, commit_hash: str) -> tuple[str, bool]:
    """ Show the details of a specific commit """
    return run_git_command(path, 'show', commit_hash)


def diff(path: Path, file: str=".") -> tuple[str, bool]:
    """ Get the diff of a specific file """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'diff', '-U10000', '--cached', file)


def go_to(path: Path, commit_hash: str) -> tuple[str, bool]:
    """ Checkout a specific commit """
    return run_git_command(path, 'checkout', commit_hash)








