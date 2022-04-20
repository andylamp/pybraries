"""Tests for `pybraries` Search class."""
from time import sleep

import pytest

import pybraries


# fixture to avoid hitting rate limit
@pytest.fixture(autouse=True, scope="function")
def wait_a_sec():
    sleep(1)
    yield


# variables for testing
# put in fixture
search = pybraries.Search()  # instantiate search api object
PKG_MGR = "pypi"  # package manager name
PKG_1 = "plotly"  # package name
PKG_2 = "yellowbrick"  # package name
GH_HOST = "github"  # host name
GH_USERNAME_TEST = "discdiver"  # GitHub username
GH_USERNAME2_TEST = "jakevdp"  # GitHub username
GH_OWNER_TEST = "notebooktoall"  # GitHub repo owner
GH_OWNER2_TEST = "pandas-dev"  # GitHub repo owner
REPO_TEST = "notebooktoall"  # repository name
REPO2_TEST = "pandas"  # repository name
REPO3_TEST = "scikit-learn"  # repo name


# Integration tests
# Platforms functionality
def test_platforms():
    """'Go' is in a returned dictionary with a key "name" when platforms are queried"""
    all_platforms = search.platforms()
    assert any("Conda" == platform["name"] for platform in all_platforms)


def test_platforms_doesnt_have_fake_platform():
    """'Go' is in a returned dictionary with a key "name" when platforms are queried"""
    all_platforms = search.platforms()
    assert not any("Cona" == platform["name"] for platform in all_platforms)


# Project functionality
def test_project_args():
    """returns a dict with correct package name"""
    pack = search.project(PKG_MGR, PKG_1)
    assert pack["name"] == "plotly"


def test_project_kwargs():
    """using kwargs - returns a dict with correct package name"""
    packs = search.project(platforms="pypi", name="plotly")
    assert packs["name"] == "plotly"


def test_project_dependencies():
    """returns a dict with correct package name"""
    pack = search.project_dependencies(PKG_MGR, PKG_1)
    assert pack["name"] == "plotly"


def test_project_dependents():
    """returns a list of dicts with correct package name"""
    packer = search.project_dependents(PKG_MGR, PKG_1)
    assert packer[0]["name"] is not None


def test_project_dependent_repositories():
    """returns a list of dicts with a description"""
    pack = search.project_dependent_repositories(PKG_MGR, PKG_2)
    assert pack[0]["description"] is not None


def test_project_contributors():
    """returns a list item with a github_id >0"""
    pack = search.project_contributors(PKG_MGR, PKG_2)
    assert float(pack[0]["github_id"]) > 0


def test_project_sourcerank():
    """returns a dict with a package with a basic_info_present key"""
    pack = search.project_sourcerank(PKG_MGR, PKG_2)
    assert pack["basic_info_present"] >= 0


def test_project_usage():
    """returns a dict with a project usage list item"""
    pack = search.project_usage(PKG_MGR, PKG_2)
    assert pack["*"] >= 0


def test_project_search():
    """Project search returns a project list item with a name key"""
    projects = search.project_search(keywords="visualization")

    assert projects


def test_project_search_with_kwargs():
    """Project search with kwargs for analytics
    and sort stars returns project with analytics as keyword"""
    projects = search.project_search(sort="stars", keywords="analytics", platforms="Pypi")
    assert "analytics" in projects[0]["keywords"]


def test_project_search_with_filters():
    """Project search with kwargs for visualization
    and sort stars returns project with visualization as keyword"""
    projects = search.project_search(keywords="visualization", sort="stars")
    assert "visualization" in projects[0]["keywords"]


# Repository functionality


def test_repository():
    """returns a project with github_id from github"""
    repos = search.repository(GH_HOST, GH_OWNER_TEST, REPO_TEST)
    assert repos["github_id"] in repos.values()


def test_repository_dependencies():
    """returns a project with full_name in keys"""
    repo_deps = search.repository_dependencies(GH_HOST, GH_OWNER2_TEST, REPO2_TEST)
    assert "full_name" in repo_deps.keys()


def test_repository_projects():
    """returns a project with name in keys"""
    repo_projs = search.repository_projects(GH_HOST, GH_OWNER2_TEST, REPO2_TEST)
    assert "name" in repo_projs[0].keys()


# User functionality


def test_user():
    """returns a repo with correct login name"""
    users = search.user(GH_HOST, GH_USERNAME_TEST)
    assert users["login"] == "discdiver"


def test_user_repositories():
    """returns a repo in a list item with size > 0"""
    user_repos = search.user_repositories(GH_HOST, GH_USERNAME_TEST)
    assert user_repos[0]["size"] > 0


def test_user_projects():
    """returns a package with rank >= 0"""
    user_pkgs2 = search.user_projects(GH_HOST, "wesm")
    assert user_pkgs2[0]["rank"] >= 0


def test_user_projects_contributions():
    """returns a project in a list item with stars >=0"""
    user_project_contribs = search.user_projects_contributions(GH_HOST, GH_USERNAME_TEST)
    assert user_project_contribs[0]["stars"] >= 0


def test_user_repository_contributions():
    """returns a project in a list item a size >= 0"""
    user_repo_contribs = search.user_repository_contributions(GH_HOST, GH_USERNAME_TEST)
    assert user_repo_contribs[0]["size"] >= 0


def test_user_dependencies():
    """returns a project in a list item with a rank >= 0"""
    user_deps = search.user_dependencies(GH_HOST, GH_USERNAME2_TEST)
    assert user_deps[0]["rank"] >= 0
