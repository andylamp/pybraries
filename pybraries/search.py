# search.py
from typing import Any

from pybraries.search_helpers import search_api


class Search:
    """Class for wrapping the libraries.io API for
    platform, project, repo, and user GET actions"""

    @staticmethod
    def platforms() -> Any:
        """
        Return a list of supported package managers.

        Returns:
            List of dicts of platforms with platform info from libraries.io.
        """

        return search_api("platforms")

    @staticmethod
    def project(platforms: str, name: str) -> Any:
        """
        Return information about a project and its versions from a platform (e.g. PyPI).

        Args:
            platforms: package manager (e.g. "pypi").
            name: project name.
        Returns:
            List of dictionaries with information about the project from libraries.io.
        """
        return search_api("project", platforms, name)

    @staticmethod
    def project_dependencies(platforms: str, project: str, version: str = None) -> Any:
        """
        Get dependencies for a version of a project.

        Returns the latest version info.

        Args:
            platforms: package manager (e.g. "pypi").
            project: project name.
            version: (optional) project version
        Returns:
            Dict of dependencies for a version of a project from libraries.io.
        """

        return search_api("project_dependencies", platforms, project, version=version)

    @staticmethod
    def project_dependents(platforms: str, project: str, version: str = None) -> Any:
        """
        Get projects that have at least one version that depends on a given project.

        Args:
            platforms: package manager (e.g. "pypi").
            project: project name
            version: project version
        Returns:
            List of dicts project dependents from libraries.io.
        """

        return search_api("project_dependents", platforms, project, version=version)

    @staticmethod
    def project_dependent_repositories(platforms: str, project: str) -> Any:
        """
        Get repositories that depend on a given project.

        Args:
            platforms: package manager (e.g. "pypi")
            project: project name
        Returns:
            List of dicts of dependent repositories from libraries.io.
        """

        return search_api("project_dependent_repositories", platforms, project)

    @staticmethod
    def project_contributors(platforms: str, project: str) -> Any:
        """
        Get users that have contributed to a given project.

        Args:
            platforms: package manager
            project: project name
        Returns:
            List of dicts of project contributor info from libraries.io.
        """

        return search_api("project_contributors", platforms, project)

    @staticmethod
    def project_sourcerank(platforms: str, project: str) -> Any:
        """
        Get breakdown of SourceRank score for a given project.

        Args:
            platforms: package manager
            project: project name
        Returns:
            Dict of sourcerank info response from libraries.io.
        """

        return search_api("project_sourcerank", platforms, project)

    @staticmethod
    def project_usage(platforms: str, project: str) -> Any:
        """
        Get breakdown of usage for a given project.

        Args:
            platforms: package manager
            project: project name
        Returns:
            Dict with info about usage from libraries.io.
        """

        return search_api("project_usage", platforms, project)

    @staticmethod
    def project_search(**kwargs):
        """
        Search for projects.
        Args - keywords only:
            keywords (str):  required argument: keywords to search
            languages (str): optional programming languages to filter
            licenses (str): license type to filter
            platforms (str):, platforms to filter

            sort str: (optional) one of rank, stars,
                dependents_count, dependent_repos_count,
                latest_release_published_at, contributions_count, created_at

        Returns:
            List of dicts of project info from libraries.io.
        """
        return search_api("special_project_search", **kwargs)

    @staticmethod
    def repository(host: str, owner: str, repo: str) -> Any:
        """
        Return information about a repository and its versions.

        Args:
            host: host provider name (e.g. GitHub)
            owner: owner
            repo: repo
        Returns:
            List of dicts of info about a repository from libraries.io.
        """

        return search_api("repository", host, owner, repo)

    @staticmethod
    def repository_dependencies(host: str, owner: str, repo: str) -> Any:
        """
        Return information about a repository's dependencies.

        Args:
            host: host provider name (e.g. GitHub)
            owner: owner
            repo: repo
        Returns:
            Dict of repo dependency info from libraries.io.
        """

        return search_api("repository_dependencies", host, owner, repo)

    @staticmethod
    def repository_projects(host: str, owner: str, repo: str) -> Any:
        """
        Get a list of projects referencing the given repository.

        Args:
            host: host provider name (e.g. GitHub)
            owner: owner
            repo: repo
        Returns:
            List of dicts of projects referencing a repo from libraries.io.
        """

        return search_api("repository_projects", host, owner, repo)

    @staticmethod
    def user(host: str, user: str) -> Any:
        """
        Return information about a user.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
        Dict of info about user from libraries.io.
        """
        return search_api("user", host, user)

    @staticmethod
    def user_repositories(host: str, user: str) -> Any:
        """
        Return information about a user's repos.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
            List of dicts with info about user repos from libraries.io.
        """
        return search_api("user_repositories", host, user)

    @staticmethod
    def user_projects(host: str, user: str) -> Any:
        """
        Return information about projects using a user's repos.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
            List of dicts of project info from libraries.io.
        """
        return search_api("user_projects", host, user)

    @staticmethod
    def user_projects_contributions(host: str, user: str) -> Any:
        """
        Return information about projects a user has contributed to.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
            List of dicts with user project contribution info from libraries.io.
        """
        return search_api("user_projects_contributions", host, user)

    @staticmethod
    def user_repository_contributions(host: str, user: str) -> Any:
        """
        Return information about repositories a user has contributed to.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
            (list): list of dicts response from libraries.io
        """
        return search_api("user_repositories_contributions", host, user)

    @staticmethod
    def user_dependencies(host, user):
        """
        Return a list of unique user's repositories' dependencies.

        Ordered by frequency of use in those repositories.

        Args:
            host: host provider name (e.g. GitHub)
            user: username
        Returns:
            List of dicts with user project dependency info.
        """
        return search_api("user_dependencies", host, user)
