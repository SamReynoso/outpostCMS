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



Functions for creating directories
'''
def make_new_canonical_dir(root_path):
    mkdir(root_path)
    touch_json(root_path, 'canonical.json', [])


def make_new_group_dir(repo_path, group):
    group_path = repo_path + "/" + group
    mkdir(group_path)
    touch_readme(group_path, 'README.md', f"# {group}")


def make_new_project_dir(group_path, project):
    project_path = group_path + '/' + project
    mkdir(project_path)
    touch_json(project_path, 'meta.json', [])


'''




Functions for creating git branches for new projects.
'''
def create_project_branch(worktree_path, group, project):
    project_branch = group+ '/' + project
    run_git_command(worktree_path, 'branch', project_branch)
    run_git_command(worktree_path, 'add', '.')
    run_git_command(worktree_path, 'commit', '-m', f'Create new project: {project_branch}')


''' 




Below are all the functions that needed to implement git into the content management system.
'''

def create_canonical_repo(root_path: str="canonical"):
    make_new_canonical_dir(root_path)
    run_git_command(root_path, 'init')
    run_git_command(root_path, 'add', '.')
    run_git_command(root_path, 'commit', '-m', 'Initializing Canonical Repository')


def create_worktree(root_path: str="canonical", working_path: str="working"):
    assert does_not_exist(working_path), f"Path already exists: {working_path}"
    run_git_command(root_path, 'worktree', 'add', working_path)


def create_new_group(group: str, working_path: str="working"):
    make_new_group_dir(working_path, group)


def create_new_project(group: str, project: str, working_path: str="working"):
    group_path = working_path + '/' +  group
    make_new_project_dir(group_path, project)
    create_project_branch(working_path, group, project)


def switch_projects(group: str, project: str, working_path: str="working"):
    project_branch = group + '/' + project
    run_git_command(working_path, 'checkout', project_branch)
    run_git_command(working_path, 'add', '.')
    run_git_command(working_path, 'commit', '-m', f'Switch to project: {project_branch}')


def save(message: str, working_path: str="working"):
    run_git_command(working_path, 'add', '.')
    run_git_command(working_path, 'commit', '-m', message)


def update(working_path: str="working"):
    run_git_command(working_path, 'merge', 'main')


def publish(group: str, project: str, canonical_path: str="canonical"):
    project_branch = group + '/' + project
    run_git_command(canonical_path, 'merge', project_branch)


def init():
    create_canonical_repo()
    create_worktree()


if __name__ == "__main__":
    group = "test_group"
    project = "test_project"

    print(f'''
    [TEST] Git Commands
    This is a test for the git commands.
          The following commands will be run:
            - git init
            - git add .
            - git commit -m "Initializing Canonical Repository"
            - git submodule add <group_path>
            - git branch <project>
            - git worktree add <working_path>

    The following paths will be created:
        - [ Canonical Repository ] ./canonical/
        - [ Working Directory    ] ./working/

    The following groups and projects will be created:
        - [Group] - directory and git repository : {group} 
        - [Project] - directory and git branch   : {project} 

    ''')

    create_new_group(group)
    create_new_project(group, project)
    switch_projects(group, project)




