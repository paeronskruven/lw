import lw.sources.blocket


def test_valid_query():
    results = lw.sources.blocket.BlocketSource().query('a')
    assert len(list(results)) > 0


def test_invalid_query():
    results = lw.sources.blocket.BlocketSource().query('abc123')
    assert len(list(results)) == 0
