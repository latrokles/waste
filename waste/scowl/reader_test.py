import datetime
import decimal
import unittest
import uuid

from .reader import EOF, CharacterStream, Reader
from .type import Condition, Form, Keyword, Symbol


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

    def test_reads_after_blankspace(self):
        self.assertEqual(self._read('    "Sakura Nagashi"'), "Sakura Nagashi")

    def test_reads_string_form(self):
        self.assertEqual(self._read('"this is a string"'), "this is a string")

    def test_returns_reader_error_condition_on_unterminated_strings(self):
        form = self._read('"this is a bad string')
        self.assertIsInstance(form, Form)
        self.assertIsInstance(form, Condition)
        self.assertEqual(form.key, Keyword("ReaderError"))

    def test_reads_numbers(self):
        self.assertEqual(self._read("1_000"), 1_000)
        self.assertEqual(self._read("0xff"), 255)
        self.assertEqual(self._read("1_000.50"), 1_000.5)
        self.assertEqual(self._read("1_000.50M"), decimal.Decimal(1_000.5))

    def test_reads_list(self):
        self.assertEqual(self._read("(1 2 3 4)"), [1, 2, 3, 4])

    def test_reads_tuple(self):
        self.assertEqual(self._read("[1 2 3 4]"), (1, 2, 3, 4))

    def test_reads_map(self):
        self.assertEqual(self._read('{"a" 1 "b" 2}'), {"a": 1, "b": 2})

    def test_reads_keyword(self):
        self.assertEqual(self._read(":foo"), Keyword("foo"))
        self.assertEqual(self._read(":user/foo"), Keyword("foo", "user"))

    def test_reads_comment(self):
        self.assertEqual(self._read("; this is a comment"), EOF)
        self.assertEqual(self._read("; this is a comment\n1_000"), 1_000)

    def test_reads_symbol(self):
        self.assertEqual(self._read("nil"), None)
        self.assertEqual(self._read("false"), False)
        self.assertEqual(self._read("true"), True)
        self.assertEqual(self._read("str/join"), Symbol("join", "str"))
        self.assertEqual(self._read("bar"), Symbol("bar"))
        self.assertEqual(self._read(".foo"), Symbol(".foo"))
        self.assertEqual(self._read("a"), Symbol("a"))

    def test_read_form(self):
        expected = [
            "a string",
            1_000,
            Symbol("foo"),
            Symbol("baz", "bar"),
            3.1459,
            decimal.Decimal(99.5),
        ]
        actual = self._read('("a string" 1_000 foo bar/baz 3.1459 99.5M)')
        self.assertEqual(actual, expected)

    def test_read_date_literal(self):
        self.assertEqual(self._read('#date "2024-11-26"'), datetime.date(2024, 11, 26))

    def test_read_datetime_literal(self):
        self.assertEqual(
            self._read('#datetime "2024-11-26T20:37:00-0000"'),
            datetime.datetime(2024, 11, 26, 20, 37, 0, tzinfo=datetime.timezone.utc),
        )

    def test_read_timestamp_seconds(self):
        self.assertEqual(
            self._read("#ts-secs 1732653420.0"),
            datetime.datetime(2024, 11, 26, 20, 37, 0, tzinfo=datetime.timezone.utc),
        )

    def test_read_timestamp_millis(self):
        self.assertEqual(
            self._read("#ts-millis 1732653420000"),
            datetime.datetime(2024, 11, 26, 20, 37, 0, tzinfo=datetime.timezone.utc),
        )

    def test_read_uuid(self):
        self.assertEqual(
            self._read('#uuid "a9782847-ae72-4645-a90e-68dd0e2d1139"'),
            uuid.UUID("a9782847-ae72-4645-a90e-68dd0e2d1139"),
        )

    def test_read_data_literal_returns_reader_error_if_unable_to_parse_literal(self):
        form = self._read('#uuid "sdasda121"')
        self.assertIsInstance(form, Condition)
        self.assertEqual(form.key, Keyword("ReaderError"))
        self.assertEqual(form.meta.get("cause"), "badly formed hexadecimal UUID string")

    def test_read_data_literal_returns_reader_error_if_no_suitable_reader_found(self):
        form = self._read('#foo "sdasda121"')
        self.assertIsInstance(form, Condition)
        self.assertEqual(form.key, Keyword("ReaderError"))

    def _read(self, source):
        return Reader(CharacterStream(source)).read_form()
