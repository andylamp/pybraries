import pytest
from pyexpect import expect

from pybraries.search import Search

DEFAULT_PER_PAGE = 30
MAX_PER_PAGE = 100
PLATFORM = "Pypi"
NAME = "flask"
PLOTLY = "plotly"
PROJECT = "plotly"


@pytest.fixture
def search():
    return Search()


def expect_correct_project(name, platform, project):
    """return the top project"""

    expect(project["stars"]).is_greater_or_equal_than(1)
    expect(project["forks"]).is_greater_or_equal_than(1)
    expect(project["dependents_count"]).is_greater_or_equal_than(0)
    expect(project["platform"]).equals(platform)
    expect(project["name"].lower()).equals(NAME)


def test_project(search):
    project = search.project(PLATFORM, NAME)
    print(f"project: {project}")
    expect_correct_project(NAME, PLATFORM, project)


def test_project_search(search, monkeypatch):
    from pybraries.helpers import sess

    old_get = sess.get

    def new_sess_get(*args, **kwargs):
        from urllib.parse import parse_qs, urlparse

        r = old_get(*args, **kwargs)
        params = parse_qs(urlparse(r.request.url).query)
        expect(params).includes("q", "api_key", "platforms")
        expect(params["q"][0]).equals(NAME)
        expect(params["platforms"][0].lower()).equals("pypi")
        return r

    monkeypatch.setattr(sess, "get", new_sess_get)

    projects = search.project_search(
        keywords="visualization", platforms="Pypi", sort="stars"
    )

    monkeypatch.undo()

    # expect_correct_project("bokeh", "Pypi", projects)


def dictfilt(x, y):
    return dict([(i, x[i]) for i in x if i in set(y)])


def test_projects(search):
    projects = search.project_search(
        sort="stars", platforms="Pypi", keywords="visualization"
    )

    # resorted_projects = sorted(
    #     projects, key=lambda project: project["dependents_count"], reverse=True
    # )
    # wanted_keys = ("name", "dependents_count")
    # print(dictfilt(projects[0], wanted_keys))
    # print(dictfilt(resorted_projects[0], wanted_keys))

    # for actual, expected in zip(projects, resorted_projects):
    #     expect(actual["dependents_count"]).is_greater_or_equal_than(
    #         expected["dependents_count"]
    #     )
    #     expect(actual["platform"]).equals("Pypi")

    expect(len(projects)).to_be(DEFAULT_PER_PAGE)


def test_projects_100_per_page(search):
    projects = search.project_search(
        sort="dependents_count",
        platforms="pypi",
        licenses="MIT",
        per_page=MAX_PER_PAGE,
        keywords=NAME,
    )
    expect(projects).of_size(MAX_PER_PAGE)
