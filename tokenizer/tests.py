from datetime import date
import unittest

import tokenizer


class TestSoundex(unittest.TestCase):
    def test_soundex(self):
        self.assertEqual(tokenizer.soundex("Bangalore"), "B524")

        # From PHP docs
        # self.assertEqual(tokenizer.soundex("Euler"), tokenizer.soundex("Ellery")) # E460
        # self.assertEqual(tokenizer.soundex("Gauss"), tokenizer.soundex("Ghosh"))  # G200
        # self.assertEqual(tokenizer.soundex("Hilbert"), tokenizer.soundex("Heilbronn"))  # H416
        # self.assertEqual(tokenizer.soundex("Knuth"), tokenizer.soundex("Kant"))  # K530
        # self.assertEqual(tokenizer.soundex("Lloyd"), tokenizer.soundex("Ladd"))  # L300
        # self.assertEqual(tokenizer.soundex("Lukasiewicz"), tokenizer.soundex("Lissajous"))  # L222

        # self.assertEqual(tokenizer.soundex("Washington"), "W252")
        # self.assertEqual(tokenizer.soundex("Lee"), "L000")
        # self.assertEqual(tokenizer.soundex("Gutierrez"), "G362")
        # self.assertEqual(tokenizer.soundex("Pfister"), "P123") # P236 according to PHP
        # self.assertEqual(tokenizer.soundex("Jackson"), "J250")
        # self.assertEqual(tokenizer.soundex("Tymczak"), "T522")
        # self.assertEqual(tokenizer.soundex("A"), "A000")
        # self.assertEqual(tokenizer.soundex("Çáŕẗéř "), "C636")
        # self.assertEqual(tokenizer.soundex("Ashcroft "), "A261")
        # self.assertEqual(tokenizer.soundex("¿"), "¿000")


class TestPIITokenizer(unittest.TestCase):
    def test_normalize(self):
        t = tokenizer.PIITokenizer()
        self.assertEqual(t.normalize("TOLOWER"), "tolower")
        self.assertEqual(t.normalize("Hello  "), "hello")
        self.assertEqual(t.normalize("  Hello"), "hello")
        self.assertEqual(t.normalize("  Hello      "), "hello")
        self.assertEqual(t.normalize("aa  bb"), "aa bb")
        self.assertEqual(t.normalize("aa     bb cc  dd"), "aa bb cc dd")
        self.assertEqual(t.normalize("hello123"), "hello123")
        self.assertEqual(t.normalize("hello123", False), "hello")
        self.assertEqual(t.normalize("hell--o__12.3à", False), "hello")

    def test_tokenize(self):
        t = tokenizer.PIITokenizer()
        tokens = t.tokenize(
            first_name="Albert", last_name="Einstein", date_of_birth="1879-03-14"
        )

        # Almost all tokens are empty
        self.assertEqual(tokens["middle_name_token"], "")
        self.assertEqual(tokens["gender_token"], "")
        self.assertEqual(tokens["country_at_birth_token"], "")
        self.assertEqual(tokens["state_at_birth_token"], "")
        self.assertEqual(tokens["city_at_birth_token"], "")
        self.assertEqual(tokens["zip_code_at_birth_token"], "")
        self.assertEqual(tokens["abbr_zip_code_at_birth_token"], "")

        # Required fields are not empty
        self.assertNotEqual(tokens["first_name_token"], "")
        self.assertNotEqual(tokens["last_name_token"], "")
        self.assertNotEqual(tokens["date_of_birth_token"], "")
        self.assertNotEqual(tokens["full_name_token"], "")
        self.assertNotEqual(tokens["first_name_soundex_token"], "")
        self.assertNotEqual(tokens["last_name_soundex_token"], "")

        # They are strings of length 1024
        self.assertEqual(len(tokens["first_name_token"]), 1024)
        self.assertEqual(len(tokens["last_name_token"]), 1024)
        self.assertEqual(len(tokens["date_of_birth_token"]), 1024)
        self.assertEqual(len(tokens["full_name_token"]), 1024)
        self.assertEqual(len(tokens["first_name_soundex_token"]), 1024)
        self.assertEqual(len(tokens["last_name_soundex_token"]), 1024)

        # Only formed by zeros and ones
        self.assertEqual(set(tokens["first_name_token"]), {"0", "1"})
        self.assertEqual(set(tokens["last_name_token"]), {"0", "1"})
        self.assertEqual(set(tokens["date_of_birth_token"]), {"0", "1"})
        self.assertEqual(set(tokens["full_name_token"]), {"0", "1"})
        self.assertEqual(set(tokens["first_name_soundex_token"]), {"0", "1"})
        self.assertEqual(set(tokens["last_name_soundex_token"]), {"0", "1"})

    def test_normalize_date_of_birth(self):
        t = tokenizer.PIITokenizer()
        self.assertEqual(t.normalize_date_of_birth("1879-03-14"), date(1879, 3, 14))

    def test_submit(self):
        t = tokenizer.PIITokenizer()
        tokens = t.tokenize(
            first_name="Albert", last_name="Einstein", date_of_birth="1879-03-14"
        )
        t.submit(
            "http://localhost:8000/v2/submit/",
            "7a26f7d4-4379-48af-9dfa-c09900afe694",
            tokens,
        )


class TestQGrams(unittest.TestCase):
    def test_bigrams(self):
        self.assertEqual(tokenizer.bigrams("hello"), ["he:1", "el:1", "ll:1", "lo:1"])
        self.assertEqual(tokenizer.bigrams(""), [""])
        self.assertEqual(tokenizer.bigrams("a"), ["a:1"])
        self.assertEqual(tokenizer.bigrams("ab"), ["ab:1", "a:1", "b:1"])
        self.assertEqual(tokenizer.bigrams("abc"), ["ab:1", "bc:1"])
        self.assertEqual(tokenizer.bigrams("aaa"), ["aa:1", "aa:2"])
        self.assertEqual(tokenizer.bigrams("aaaa"), ["aa:1", "aa:2", "aa:3"])
        self.assertEqual(
            tokenizer.bigrams("barbara"),
            ["ba:1", "ar:1", "rb:1", "ba:2", "ar:2", "ra:1"],
        )
        self.assertEqual(
            tokenizer.bigrams("he llo"), ["he:1", "e :1", " l:1", "ll:1", "lo:1"]
        )


if __name__ == "__main__":
    unittest.main()
