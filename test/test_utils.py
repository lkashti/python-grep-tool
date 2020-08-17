import pytest
from tool import search



@pytest.mark.parametrize(
    'lines,regex,expected',
    [
        (
            ['testline1'], 'tli',
            (0, 'testline1', 'tli', 3)
        ),
        (
            ['testline1', 'testline2'], 'ne2',
            (1, 'testline2', 'ne2', 6)
        ),
        (
            ['testline1'], '',
            (0, 'testline1', '', 0)
        ),

    ]
)
def test_search(lines, regex, expected):
    result = next(search(lines, regex))
    assert result == expected


@pytest.mark.parametrize(
    'lines,regex,expected',
    [
        (
            [], 'ne2',
            StopIteration
        ),
    ]
)
def test_search_exception(lines, regex, expected):
    with pytest.raises(StopIteration) as exc_info:
        next(search(lines, regex))
    assert exc_info.type == expected
