"""
run with: 
python -m unittest waste_test.py

if covergage is available
coverage run -m unittest waste_test.py
coverate html
"""

import unittest

import waste as w

class StringReaderTest(unittest.TestCase):
    def test_reads_a_single_quote_delimited_string(self):
        stream = w.CharStream("'this is a string'")
        self.assertEqual(
            w.StringReader().invoke(w.Reader(stream)),
            "this is a string",
        )

    def test_raises_error_on_unterminated_string(self):
        stream = w.CharStream("'this is a string")
        with self.assertRaises(RuntimeError):
            w.StringReader().invoke(w.Reader(stream))



        


