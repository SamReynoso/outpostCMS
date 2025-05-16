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


# Create the meta.json file in the project directory
def create_meta_json(path, group_name, project_name):
    group_path = path + '/' + group_name
    project_path = group_path + '/' + project_name
    if not os.path.exists(group_path):
        mkdir(group_path)
    mkdir(project_path)
    touch_json(project_path, 'meta.json', {})


'''




Inistialization
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
'''



CMS helpers
'''
def has_changes(path):
    changes = run_git_command(path, 'status', '--porcelain')
    return bool(changes)


def unique_project(path, group, project):
    project_path = path + '/' + group + '/' + project
    if os.path.exists(project_path):
        return False
    return True

def change_log(path, group, project):
    project_dir =  group + '/' + project
    print(f"[INFO] Getting change log for {project_dir}")
    return run_git_command(path, 'log', '--', project_dir)


'''




CMS Main Workflow
'''
def save(path, message):
    run_git_command(path, 'add', '.')
    run_git_command(path, 'commit', '-m', message)


def auto_save(path):
    if has_changes(path):
        save(path, "Changes saved automatically")


def submit(publish_path, group_name, project_name):
    branch_name = group_name + '/' + project_name
    run_git_command(publish_path, 'merge', branch_name)


def new_project(working_path, group_name, project_name):
    group_path = working_path + '/' + group_name
    project_path = group_path + '/' + project_name
    branch_name = group_name + '/' + project_name

    auto_save(working_path)
    run_git_command(working_path, 'checkout', '-b', branch_name)
    create_meta_json(working_path, group_name, project_name)
    save(project_path, f"Project '{project_name}' created in group '{group_name}'")


def change_project(working_path, group_name, project_name):
    branch_name = group_name + '/' + project_name

    auto_save(working_path)
    run_git_command(working_path, 'checkout', branch_name)


'''



test
'''
if __name__ == "__main__":
    group_1 = "group-1"
    project_1 = "project-1"

    group_2 = "group-2"
    project_2 = "project-2"

    print('''
    [TEST] Git Commands

''')

    init()
    #new_project("canonical/working", group_1, project_1)
    #new_project("canonical/working", group_2, project_1)
    #new_project("canonical/working", group_2, project_2)
    #change_project("canonical/working", group_1, project_1)
    #submit("canonical/publish", group_2, project_2)
    #print(change_log("canonical/working", group_2, project_2))
    #save("canonical/working", "Test commit 1")
    #save("canonical/working", "Test commit 2")
    #save("canonical/working", "Test commit 3")
    #submit("canonical/publish", group_2, project_2)


