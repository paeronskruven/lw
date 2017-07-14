import lw.sources.tradera


def test_valid_query():
    results = lw.sources.tradera.TraderaSource().query('a')
    assert len(list(results)) > 0


def test_invalid_query():
    results = lw.sources.tradera.TraderaSource().query('abc123')
    assert len(list(results)) == 0
