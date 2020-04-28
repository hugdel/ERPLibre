import git
from git import Repo
import argparse
import os

from script.git_tool import GitTool

CST_GITHUB_TOKEN = "GITHUB_TOKEN"
CST_BASE_BRANCH = "12.0"
CST_STABLE_BRANCH = f"{CST_BASE_BRANCH}_stable"
CST_DEV_BRANCH = f"{CST_BASE_BRANCH}_dev"


# todo 1 - lister les modules du repo Santelibre
# todo 2 - pour chq repo, vérifier si les brach stable et dev existent
# todo 3 - si n'existe pas, les créer
# todo 4 - si la branche 12.0 n'existe pas, lancer un warning


def get_config():
    """Parse command line arguments, extracting the config file name,
    returning the union of config file and command line arguments

    :return: dict of config file settings and command line arguments
    """
    # TODO update description
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
''',
        epilog='''\
'''
    )

    parser.add_argument('-d', '--dir', dest="dir", default="./",
                        help="Path of repo to change remote, including submodule.")
    args = parser.parse_args()
    return args


def main():
    config = get_config()
    lst_repo = GitTool.get_repo_info_submodule(repo_path=config.dir)
    i = 0
    total = len(lst_repo)
    for repo in lst_repo:
        i += 1
        print(f"Nb element {i}/{total}")
        url = repo.get("url")
        try:
            working_repo = Repo(repo.get("relative_path"))

        except git.exc.NoSuchPathError:
            print(f"creating repo {repo.get('name')}")
            os.mkdir(repo.get("relative_path"))
            working_repo = clone_repo(repo, CST_STABLE_BRANCH,CST_BASE_BRANCH)
            pass

        except git.exc.InvalidGitRepositoryError:
            working_repo = clone_repo(repo, CST_STABLE_BRANCH,CST_BASE_BRANCH)
            pass

        if working_repo:
            if not CST_STABLE_BRANCH in working_repo.branches:
                create_branch(working_repo,CST_BASE_BRANCH,CST_STABLE_BRANCH)
            if not CST_DEV_BRANCH in working_repo.branches:
                create_branch(working_repo,CST_STABLE_BRANCH,CST_DEV_BRANCH)


def create_branch(repo, ref_branch, dest_branch):




def clone_repo(repo, branch='', alternate_branch=''):
    if branch == '':
        raise ValueError("No branch set")
    else:
        try:
            working_repo = Repo.clone_from(repo.get("url"), repo.get("relative_path"), branch=branch)
            return working_repo
        except Exception as e:
            if alternate_branch == '':
                print(e.stderr)
                return None
            else:
                working_repo = clone_repo(repo, alternate_branch)
                return working_repo



if __name__ == '__main__':
    main()
