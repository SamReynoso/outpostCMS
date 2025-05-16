import os
import json
import subprocess


'''



git runner
'''
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
        print(f"---- Output: {e.output}")
        print()


'''



file system helpers
'''
def does_not_exist(path):
    if os.path.exists(path):
        print(f"Path already exists: {path}")
        raise Exception("Path already exists")
    return True


def mkdir(path):
    assert does_not_exist(path), f"Path already exists: {path}"
    print(f"[INFO] Creating directory: {path}")
    os.makedirs(path, exist_ok=False)


def write(file_path, content):
    assert does_not_exist(file_path), f"Path already exists: {file_path}"
    with open(file_path, 'w') as f:
        print(f"[INFO] Creating new file: {file_path}")
        f.write(content)


def touch_json(path, file_name, content):
    file_path = path + '/' + file_name
    write(file_path, json.dumps(content, indent=4))


def touch_readme(path, file_name, content):
    file_path = path + '/' + file_name
    write(file_path, content)
'''



'''
def init_git_repo(path):
    run_git_command(path, 'init')


def commit(path, message):
    run_git_command(path, 'add', '.')
    run_git_command(path, 'commit', '-m', message)


def init_worktree(path, branch_name):
    working_path = f"../{branch_name}"
    run_git_command(path, 'worktree', 'add', working_path, branch_name)


def init():
    root = "canonical"
    publish_name = "publish"
    working_name = "working"
    repo_path = root + '/' + publish_name
    mkdir(root)
    mkdir(repo_path)
    touch_json(repo_path, 'canonical.json', [])
    init_git_repo(repo_path)
    commit(repo_path, "Initializing Canonical Repository")
    run_git_command(repo_path, 'branch', working_name)
    init_worktree(repo_path, working_name)


'''



Content Management System Operations
'''
def save(path, message):
    run_git_command(path, 'add', '.')
    run_git_command(path, 'commit', '-m', message)


def auto_save(path):
    changes = run_git_command(path, 'status' '--porcelain')
    if not changes:
        print("No changes to save")
        return
    save(path, "Changes saved automatically")


def publish(working_path, group_name, project_name):
    branch_name = group_name + '/' + project_name
    run_git_command(working_path, 'merge', '--force', branch_name)


def new_project(working_path, group_name, project_name):
    group_path = working_path + '/' + group_name
    project_path = group_path + '/' + project_name
    branch_name = group_name + '/' + project_name

    auto_save(working_path)

    run_git_command(working_path, 'checkout', '-b', branch_name)
    if not os.path.exists(group_path):
        mkdir(group_path)
    mkdir(project_path)
    touch_json(project_path, 'meta.json', {})
    save(project_path, f"Project '{project_name}' created in group '{group_name}'")


def change_project(working_path, group_name, project_name):
    current_branch = run_git_command(working_path, 'branch', '--show-current')
    if current_branch == 
    auto_save(working_path)

    group_path = working_path + '/' + group_name
    project_path = group_path + '/' + project_name

    if not os.path.exists(group_path):
        mkdir(group_path)
    mkdir(project_path)
    touch_json(project_path, 'meta.json', {})
    run_git_command(working_path, 'add', '.')
    run_git_command(working_path, 'commit', '-m', f"Adding {project_name} to {group_name}")

'''



test
'''
if __name__ == "__main__":
    group = "group-1"
    project = "project-1"

    print('''
    [TEST] Git Commands

  ''')

    init()

    new_project("canonical/working", group, project)


























