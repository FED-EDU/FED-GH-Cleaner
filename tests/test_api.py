import responses

from gh_cleaner.api import GitHubAPI, GitHubAPIError


@responses.activate
def test_list_runs_and_auth_header():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/actions/runs",
        json={"workflow_runs": [{"id": 1}]},
        status=200,
    )
    api = GitHubAPI("secret")
    assert next(iter(api.list_runs("o/r")))["id"] == 1
    assert responses.calls[0].request.headers["Authorization"] == "Bearer secret"


@responses.activate
def test_delete_run():
    responses.add(responses.DELETE, "https://api.github.com/repos/o/r/actions/runs/1", status=204)
    GitHubAPI("secret").delete_run("o/r", 1)


@responses.activate
def test_error():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/actions/runs",
        json={"message": "no"},
        status=404,
    )
    try:
        list(GitHubAPI("secret").list_runs("o/r"))
        assert False
    except GitHubAPIError as exc:
        assert exc.status_code == 404
