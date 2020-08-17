from lib.formatter import (MachineReadableFormatter, ColoredFormatter,
                           SimpleFormatter, InvalidInputException)
import pytest


@pytest.mark.parametrize(
    'file_name,line_no,line,expected',
    [
        (
                'file_name', 0, 'text', 'file_name:0:text'
        ),
    ]
)
def test_simple_formatter(file_name, line_no, line, expected):
    result = SimpleFormatter(file_name, line_no, line).format()
    assert result == expected


@pytest.mark.parametrize(
    'file_name,line_no,line,expected',
    [
        (
                '', 0, 'text', 'missing file name'
        ),
        (
                'file_name', '', 'text', 'line_no should be an integer'
        ),
        (
                'file_name', 0, '', 'missing line'
        ),
    ]
)
def test_simple_formatter_exception(file_name, line_no, line, expected):
    with pytest.raises(InvalidInputException) as e:
        SimpleFormatter(file_name, line_no, line).format()
    assert str(e.value) == expected


@pytest.mark.parametrize(
    'file_name,line_no,matched_line,start_pos,expected',
    [
        (
                'file_name', 0, 'testline', 5, 'file_name:0:5:testline'
        )
    ]
)
def test_machine_readable_formatter(file_name, line_no, matched_line,
                                    start_pos, expected):
    result = MachineReadableFormatter(file_name, line_no, matched_line,
                                      start_pos).format()
    assert expected == result


@pytest.mark.parametrize(
    'file_name,line_no,matched_line,start_pos,expected',
    [
        (
                'file_name', 0, 'testline', '',
                'start_pos should be an integer'
        ),
    ]
)
def test_machine_readable_formatter_exception(file_name, line_no, matched_line,
                                              start_pos, expected):
    with pytest.raises(InvalidInputException) as e:
        MachineReadableFormatter(file_name, line_no, matched_line,
                                 start_pos).format()
    assert str(e.value) == expected


@pytest.mark.parametrize(
    'line, regex_result, expected',
    [
        (
                'testline', 'tli',
                'tes' + ColoredFormatter.colors.red + 'tli'
                + ColoredFormatter.colors.RESET + 'ne'
        ),
    ]
)
def test_colored_formatter(line, regex_result, expected):
    result = ColoredFormatter(line, regex_result).format()
    assert expected == result


@pytest.mark.parametrize(
    'line,regex_result,expected',
    [
        (
                '', 'tli', 'missing line'
        ),
        (
                'testline', '', 'missing regex_result'
        )
    ]
)
def test_colored_formatter_exception(line, regex_result, expected):
    with pytest.raises(InvalidInputException) as e:
        ColoredFormatter(line, regex_result).format()
    assert str(e.value) == expected
