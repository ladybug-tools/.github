import sys
import os
import subprocess
import pathlib


ACCESS_TOKEN = os.getenv('GH_TOKEN', "")
ORGANIZATION_NAME = 'ladybug-tools'

def get_workflow_templates():
    workflow_templates = {}
    templates_folder = 'workflow-templates'
    for file in os.listdir(templates_folder):
        if file.endswith('.yaml') or file.endswith('.yml'):
            with open(os.path.join(templates_folder, file), 'r') as f:
                workflow_templates[file] = f.read()
    return workflow_templates

WORKFLOW_TEMPLATES = get_workflow_templates()


def clone_repository(repo_name: str) -> pathlib.Path:
    clone_url = f"https://{ACCESS_TOKEN}@github.com/{ORGANIZATION_NAME}/{repo_name}.git"
    os.makedirs('tmp', exist_ok=True)
    repo_path = pathlib.Path(f'tmp/{repo_name}').absolute()
    subprocess.call(["git", "clone", clone_url, repo_path.as_posix()])
    return repo_path

def replace_templates_in_repository(repo_path: pathlib.Path):
    workflows_path = repo_path.joinpath('.github', 'workflows') 
    
    if not workflows_path.exists():
        workflows_path = workflows_path.joinpath('..').resolve()

    if not workflows_path.exists():
        return

    for file in os.listdir(workflows_path.as_posix()):
        if file in WORKFLOW_TEMPLATES:
            print(f"Updating workflow template: {file}")
            with open(workflows_path.joinpath(file).as_posix(), 'w') as f:
                f.write(WORKFLOW_TEMPLATES[file])


def add_commit_and_push(repo_path: pathlib.Path):
    cwd = repo_path.as_posix()
    repo_name =  os.path.basename(os.path.normpath(repo_path))
    print(f"fake git add and push to {repo_name}")
    # subprocess.call(["git", "add", "."], cwd=cwd)
    # subprocess.call(["git", "commit", "-m", 'ci(actions): update workflows from templates'], cwd=cwd)
    # push_url = f"https://{ACCESS_TOKEN}@github.com/{ORGANIZATION_NAME}/{repo_name}.git"
    # subprocess.call(["git", "push", push_url], cwd=cwd)
    
def update_repo(repo_name):
    repo_path = clone_repository(repo_name)
    replace_templates_in_repository(repo_path)
    add_commit_and_push(repo_path)

if __name__ == "__main__":
    repo = sys.argv[1]
    update_repo(repo)