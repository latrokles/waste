import unittest

from .reader import CharacterStream, Reader
from .type import Condition, Form, Symbol


class TestCharacterStream(unittest.TestCase):
    def setUp(self):
        self.stream = CharacterStream("(defn add [a b] (+ a b))")
        self.empty_stream = CharacterStream("")
        self.multiline_stream = CharacterStream("\n[1 2]")

    def test_peek_returns_character_but_does_not_avdance_position(self):
        current = self.stream.location
        self.assertEqual(self.stream.peek(), "(")
        self.assertEqual(self.stream.location, current)

    def test_peek_returns_empty_string_when_at_end_of_stream(self):
        self.assertEqual(self.empty_stream.peek(), "")

    def test_read_returns_char_at_current_pos_and_advances_pos(self):
        self.assertEqual(self.stream.read(), "(")
        self.assertEqual(self.stream.location, (1, 2))
        self.assertEqual(self.multiline_stream.read(), "\n")
        self.assertEqual(self.multiline_stream.location, (2, 1))

    def test_read_returns_empty_string_and_does_not_advance_when_at_end_of_stream(self):
        self.assertEqual(self.empty_stream.read(), "")
        self.assertEqual(self.empty_stream.location, (1, 1))

    def test_step_back_moves_back_position_in_stream(self):
        current_stream_l0 = self.stream.location
        c = self.stream.read()
        self.stream.step_back()
        self.assertEqual(self.stream.location, current_stream_l0)
        self.assertEqual(self.stream.read(), c)

        current_multiline_l0 = self.multiline_stream.location
        mc = self.multiline_stream.read()
        self.multiline_stream.step_back()
        self.assertEqual(self.multiline_stream.location, current_multiline_l0)
        self.assertEqual(self.multiline_stream.read(), mc)


class TestReader(unittest.TestCase):
    def test_returns_eof_at_eof(self):
        self.assertEqual(Symbol("#EOF#", "reader"), self._read(""))

    def test_reads_string_form(self):
        self.assertEqual(self._read('"this is a string"'), "this is a string")

    def test_returns_reader_error_condition_on_unterminated_strings(self):
        form = self._read('"this is a bad string')
        self.assertIsInstance(form, Form)
        self.assertIsInstance(form, Condition)
        self.assertEqual(form.key, "ReaderError")

    def test_returns_reader_error_condition_if_no_suitable_reader_found(self):
        form = self._read("5000")
        self.assertIsInstance(form, Form)
        self.assertIsInstance(form, Condition)
        self.assertEqual(form.key, "ReaderError")

    def _read(self, source):
        return Reader(CharacterStream(source)).read_form()
