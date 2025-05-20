import subprocess
from pathlib import Path


def run_git_command(path: Path, *args) -> tuple[str, bool]:
    try:
        print(f"[DEBUG] Running git command: {' '.join(['git'] + list(args))} in {path}")
        result = subprocess.run(
            ['git'] + list(args),
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip(), True
    except subprocess.CalledProcessError as e:
        return e.stderr.strip(), False


def branch(path: Path, branch: str) -> tuple[str, bool]:
    """ Equivalent to 'git checkout -b <branch>' """
    run_git_command(path, 'checkout', '-b', branch)
    return head(path)


def branch_name(path: Path) -> tuple[str, bool]:
    """ Equivalent to 'git rev-parse --abbrev-ref HEAD' """
    return run_git_command(path, 'rev-parse', '--abbrev-ref', 'HEAD')


def head(path: Path) -> tuple[str, bool]:
    """ Equivalent to 'git rev-parse HEAD' """
    return run_git_command(path, 'rev-parse', 'HEAD')


def add(path: Path) -> tuple[str, bool]:
    """ Equivalent to 'git add .' """
    return run_git_command(path, 'add', '.')


def log(path: Path, branch: str) -> tuple[str, bool]:
    """ Equivalent to 'git log --oneline <branch>' """
    return run_git_command( path, 'log', '--oneline', '--', branch,)

def checkout(path: Path, identifier: str) -> tuple[str, bool]:
    """ Equivalent to 'git checkout <identifier>' """
    return run_git_command(path, 'checkout', identifier)


def status(path: Path) -> tuple[str, bool]:
    """ Equivalent to 'git status --porcelain' """
    return run_git_command( path, 'status', '--porcelain',)

def commit(path: Path, message: str="Changes saved automatically") -> tuple[str, bool]:
    """ Equivalent to 'git add .; git commit -m <message>' """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'commit', '-m', message)

def merge(path: Path, branch: str, message: str="Merging changes") -> tuple[str, bool]:
    """ Equivalent to 'git merge <branch>' """
    return run_git_command(path, 'merge', branch, '-m', message)


def show(path: Path, hash: str) -> tuple[str, bool]:
    """ Equivalent to 'git show <hash>' """
    return run_git_command(path, 'show', hash)


def diff(path: Path, file: str=".") -> tuple[str, bool]:
    """ Equivalent to 'git add .; git diff -U10000 --cached <file>' """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'diff', '-U10000', '--cached', file)
