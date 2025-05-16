import os
import json
import subprocess

PUBLISH_REPOSITORY_README = """
# Publish Repository
This README should help you understand the purpose of this repository. This repo is the target of the CMS API when
serving content in production mode. This repository is the canonical repository for the CMS API. Works in progress
should be done in the working directory. This worktree has a different branch for each project which can be merged
into main in the publish directory. The publish directory should always have main checked out.
"""

WORKING_REPOSITORY_README = """
# Working Worktree
The working directory holds all works in progress. The server does not access this directory when in production mode.
changes made through the browser interface should ensure that each project branch only contains changes related to the
corresponding project directory. With the main branch always being checked out in the publish branch you should feel
secure that none of your work will be served to the client until you are ready to publish and merge them into main.
"""

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


def touch_ignore(path):
    file_path = path + '/' + '.gitignore'
    content = '''
# Ignore all files
README.md
'''
    write(file_path, content)


def touch_readme(path, content):
    file_path = path + '/' + 'README.md'
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
    # Create the canonical repository and site map file 'site-map.json'
    root = "canonical"
    mkdir(root)
    touch_json(root, 'site-map.json', [])

    # Create the canonical repository 
    publish_name = "publish"
    repo_path = root + '/' + publish_name
    mkdir(repo_path)
    touch_ignore(repo_path)
    touch_readme(repo_path, PUBLISH_REPOSITORY_README)
    init_git_repo(repo_path)
    commit(repo_path, "Initializing Canonical Repository")

    # Create the worktree for the working repository
    working_name = "working"
    run_git_command(repo_path, 'branch', working_name)
    init_worktree(repo_path, working_name)
    touch_readme(root + '/' + working_name, WORKING_REPOSITORY_README)


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
    return run_git_command(path, 'log', '--pretty=format:"%h %ad %s"', '--date=iso', project_dir)


def show(path, commit_hash):
    print(f"[INFO] Showing changes for {commit_hash}")
    return run_git_command(path, 'show', commit_hash)


def go_to(path, commit_hash):
    print(f"[INFO] Checking out {commit_hash}")
    run_git_command(path, 'checkout', commit_hash)


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


