import git
from git import Repo
import argparse
import os
from warnings import warn
from tqdm import tqdm

from script.git_tool import GitTool

CST_GITHUB_TOKEN = "GITHUB_TOKEN"
CST_BASE_BRANCH = "12.0"
CST_STABLE_BRANCH = f"{CST_BASE_BRANCH}_stable"
CST_DEV_BRANCH = f"{CST_BASE_BRANCH}_dev"
CST_debug = False


# 1 - lister les modules du repo Santelibre
# 2 - pour chq repo, vérifier si les brach stable et dev existent
# todo 3 - si n'existe pas, les créer
# 4 - si la branche 12.0 n'existe pas, lancer un warning


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
    skipped_repos = []
    # total = len(lst_repo)
    for repo in tqdm(lst_repo):
        # i += 1
        # print(f"Nb element {i}/{total}")
        url = repo.get("url")
        try:
            working_repo = Repo(repo.get("relative_path"))

        except git.exc.NoSuchPathError:
            # print(f"creating repo {repo.get('name')}")
            os.mkdir(repo.get("relative_path"))
            working_repo = clone_repo(repo, CST_STABLE_BRANCH, CST_BASE_BRANCH)

        except git.exc.InvalidGitRepositoryError:
            working_repo = clone_repo(repo, CST_STABLE_BRANCH, CST_BASE_BRANCH)

        if working_repo:
            if len(working_repo.untracked_files) > 0:
                skipped_repos.append((repo, 'Untracked files in the repo'))
            else:
                if not CST_STABLE_BRANCH in working_repo.branches:
                    stable = create_branch(working_repo, CST_BASE_BRANCH, CST_STABLE_BRANCH)
                    set_default_branch(working_repo, CST_STABLE_BRANCH)
                if not CST_DEV_BRANCH in working_repo.branches:
                    dev = create_branch(working_repo, CST_STABLE_BRANCH, CST_DEV_BRANCH)

                if not stable or not dev:
                    skipped_repos.append((repo, f'Branch stable is {stable} and dev is {dev}'))
        else:
            skipped_repos.append((repo, 'Has no 12.0 Branch'))

    print('Script ended, here is the summary of skipped or incomplete repo')

    for repo, message in skipped_repos:
        print(f"{repo.get('name')} : {message}")


def change_branch(working_repo, branch):
    if not branch in working_repo.branches:
        return False
    elif len(working_repo.untracked_files) > 0:
        if CST_debug:
            warn(f'{working_repo.active_branch.name} has untracked files')
        return False
    else:
        pass
    return True


def create_branch(working_repo, ref_branch, dest_branch):
    if working_repo.active_branch.name == ref_branch:
        is_ref = True
    else:
        is_ref = change_branch(working_repo, ref_branch)

    if is_ref:
        new_branch = working_repo.create_head(dest_branch)
        new_branch.set_commit('HEAD~1').commit == working_repo.active_branch.commit.parents[0]
        return new_branch
    else:

        if CST_debug:
            print('\n')
            warn(f'Branch {dest_branch} was not created for {working_repo.working_dir}\m')
        return False


def set_default_branch(repo, branch_name):
    # todo implement setting as default
    pass


def clone_repo(repo, branch='', alternate_branch=''):
    if branch == '':
        raise ValueError("No branch set")
    else:
        try:
            working_repo = Repo.clone_from(repo.get("url"), repo.get("relative_path"), branch=branch)
            return working_repo
        except Exception as e:
            if alternate_branch == '':
                if CST_debug:
                    print(e.stderr)
                return None
            else:
                working_repo = clone_repo(repo, alternate_branch)
                return working_repo


if __name__ == '__main__':
    main()
