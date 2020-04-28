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
            pass

        except git.exc.InvalidGitRepositoryError:
            try:
                working_repo = Repo.clone_from(repo.get("url"), repo.get("relative_path"), branch=CST_BASE_BRANCH)
            except Exception as e:
                pass




if __name__ == '__main__':
    main()
