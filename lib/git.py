import subprocess


def run_git_command(path, *args) -> tuple[str, bool]:
    print(f"[INFO] Running git command: {' '.join(['git'] + list(args))} in {path}")
    try:
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


def branch(path: str, branch: str) -> tuple[str, bool]:
    """ Create a new branch and switch to it """
    commit(path, "Creating branch")
    return run_git_command(path, 'checkout', '-b', branch)


def checkout(path: str, branch: str) -> tuple[str, bool]:
    """ Switch to an existing branch """
    commit(path, "Switching branches")
    return run_git_command(path, 'checkout', branch)


def status(path: str) -> tuple[str, bool]:
    """ Get the status of the repository """
    return run_git_command(
            path,
            'status',
            '--porcelain',
            )

def commit(path: str, message: str="Changes saved automatically") -> tuple[str, bool]:
    """ Commit changes to the repository """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'commit', '-m', message)


def merge(path: str, branch: str, message: str="Merging changes") -> tuple[str, bool]:
    """ Merge changes from another branch """
    commit(path, message)
    checkout(path, 'main')
    return run_git_command(path, 'merge', branch)


def show(path: str, commit_hash: str) -> tuple[str, bool]:
    """ Show the details of a specific commit """
    return run_git_command(path, 'show', commit_hash)


def head(path: str) -> tuple[str, bool]:
    """ Get the current commit hash """
    return run_git_command(path, 'rev-parse', 'HEAD')

def hash(path: str) -> tuple[str, bool]:
    """ Get the current commit hash """
    return run_git_command(path, 'rev-parse', 'HEAD')


def diff(path: str, file: str) -> tuple[str, bool]:
    """ Get the diff of a specific file """
    run_git_command(path, 'add', '.')
    return run_git_command(path, 'diff', '-U10000', '--cached', file)


def go_to(path: str, commit_hash: str) -> tuple[str, bool]:
    """ Checkout a specific commit """
    return run_git_command(path, 'checkout', commit_hash)








