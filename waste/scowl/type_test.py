import unittest

from .type import Keyword, Symbol


class TestSymbol(unittest.TestCase):
    def test_two_symbols_with_same_name_and_package_are_equal(self):
        self.assertEqual(Symbol("join", "str"), Symbol("join", "str"))

    def test_two_symbols_with_same_name_but_diff_package_are_not_equal(self):
        self.assertNotEqual(Symbol("join", "str"), Symbol("join", "collection"))

    def test_two_symbols_with_same_package_but_diff_name_are_not_equal(self):
        self.assertNotEqual(Symbol("split", "str"), Symbol("join", "str"))

    def test_symbol_and_other_object_are_not_equal(self):
        self.assertNotEqual(Symbol("join", "str"), Keyword("foo"))

    def test_representation(self):
        self.assertEqual(repr(Symbol("join", "str")), "#'str/join")


class TestKeyword(unittest.TestCase):
    def test_two_keywords_with_same_name_and_no_package_are_equal(self):
        self.assertEqual(Keyword("foo"), Keyword("foo"))

    def test_two_keywords_with_same_name_and_same_package_are_equal(self):
        self.assertEqual(Keyword("foo", "bar"), Keyword("foo", "bar"))

    def test_two_keywords_with_same_name_but_diff_package_are_not_equal(self):
        self.assertNotEqual(Keyword("foo", "bar"), Keyword("foo", "baz"))

    def test_two_keywords_with_same_package_but_diff_name_are_not_equal(self):
        self.assertNotEqual(Keyword("foos", "bar"), Keyword("foo", "bar"))

    def test_keyword_and_other_object_are_not_equal(self):
        self.assertNotEqual(Keyword("foo"), Symbol("join", "str"))

    def test_representation(self):
        self.assertEqual(repr(Keyword("name")), ":name")
        self.assertEqual(repr(Keyword("name", "person")), ":person/name")
