"""
formatter.py - text formatters for various outputs.
"""

from abc import ABC, abstractmethod
from collections import namedtuple


class AbstractFormatter(ABC):
    """
    Defines what functionality an inheriting formatter must have.
    """

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def _validate(self):
        pass


class SimpleFormatter(AbstractFormatter):
    """Common base class for a formatter."""

    def __init__(self, file_name, line_no, matched_line):
        """
        :param str file_name: file name to be entered in the format
        :param int line_no: line number
        :param str matched_line: string with text content
        """
        self._file_name = file_name
        self._line_no = line_no
        self._matched_line = matched_line

    def format(self):
        """

        Formats the class variables to:
        file_name:line_no:matched_line

        :return: formatted string
        """
        self._validate()
        return (f'{self._file_name}:'
                f'{self._line_no}:'
                f'{self._matched_line.strip(" ")}')

    def _validate(self):
        """
        Validates that input exists.

        :raises InvalidInputException:
        """
        if not self._file_name:
            raise InvalidInputException('missing file name')
        elif not isinstance(self._line_no, int):
            raise InvalidInputException('line_no should be an integer')
        elif not self._matched_line:
            raise InvalidInputException('missing line')
        else:
            pass

    def __str__(self):
        return self.format()


class MachineReadableFormatter(SimpleFormatter):
    """Creates a machine readable string format."""

    def __init__(self, file_name, line_no, matched_line, start_pos):
        """
        :param file_name: file name to be entered in the format
        :param line_no: line number
        :param matched_line: string with text content
        :param start_pos: starting position of the matching substring
        """
        super().__init__(file_name, line_no, matched_line)
        self._start_pos = start_pos

    def format(self):
        """
        Formats the class variables to:
        file_name:line_no:start_pos:matched_line
        :return: machine readable formatted string
        """
        self._validate()
        return (f'{self._file_name}:'
                f'{self._line_no}:'
                f'{self._start_pos}:'
                f'{self._matched_line.strip(" ")}')

    def _validate(self):
        """
        Validates that input exists.

        :raises InvalidInputException:
        """
        super()._validate()
        if not isinstance(self._start_pos, int):
            raise InvalidInputException('start_pos should be an integer')

    def __str__(self):
        return self.format()


class ColoredFormatter(AbstractFormatter):
    """
    Colors a substring in a given line and regex
    """
    Color = namedtuple('Color', ['red', 'RESET'])
    colors = Color('\033[0;31m', '\033[0m')

    def __init__(self, matched_line, regex_result):
        """

        :param matched_line: string with text content
        :param regex_result: substring that matches regex query
        """
        self._matched_line = matched_line
        self._regex_result = regex_result

    def format(self):
        """
        Injects color to a substring.

        :return:
        """
        self._validate()
        colored_line = (self._matched_line.replace(self._regex_result,
                                                   f'{self.colors.red}'
                                                   f'{self._regex_result}'
                                                   f'{self.colors.RESET}'))
        return colored_line.strip(' ')

    def _validate(self):
        """

        :raises InvalidInputException:
        """
        if not self._matched_line:
            raise InvalidInputException('missing line')
        elif not self._regex_result:
            raise InvalidInputException('missing regex_result')

    def __str__(self):
        return self.format()


class InvalidInputException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        return None
