from tests.factories import UserFactory, PortfolioFactory
from atst.routes import match_url_pattern


def test_root_redirects_if_user_is_logged_in(client, user_session):
    user_session(UserFactory.create())
    response = client.get("/", follow_redirects=False)
    assert "home" in response.location


def test_match_url_pattern(client):

    assert not match_url_pattern(None)
    assert match_url_pattern("/home") == "/home"

    portfolio = PortfolioFactory()
    # matches a URL with an argument
    assert (
        match_url_pattern(f"/portfolios/{portfolio.id}")  # /portfolios/<portfolio_id>
        == f"/portfolios/{portfolio.id}"
    )
    # matches a url with a query string
    assert (
        match_url_pattern(f"/portfolios/{portfolio.id}?foo=bar")
        == f"/portfolios/{portfolio.id}?foo=bar"
    )
    # matches a URL only with a valid method
    assert not match_url_pattern(f"/portfolios/{portfolio.id}/edit")
    assert (
        match_url_pattern(f"/portfolios/{portfolio.id}/edit", method="POST")
        == f"/portfolios/{portfolio.id}/edit"
    )

    # returns None for URL that doesn't match a view function
    assert not match_url_pattern("/pwned")
    assert not match_url_pattern("http://www.hackersite.com/pwned")
