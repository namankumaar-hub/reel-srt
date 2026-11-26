import unittest

from reel_srt import build_srt, chunk_script, fmt_time


class TestReelSrt(unittest.TestCase):
    def test_fmt_time(self):
        self.assertEqual(fmt_time(0), "00:00:00,000")
        self.assertEqual(fmt_time(61.5), "00:01:01,500")

    def test_chunks_respect_sentences(self):
        self.assertEqual(
            chunk_script("one two three. four five", max_words=4),
            ["one two three.", "four five"],
        )

    def test_hindi_danda_splits(self):
        self.assertEqual(
            chunk_script("नमस्ते दोस्तों। आज नया वीडियो", max_words=4),
            ["नमस्ते दोस्तों।", "आज नया वीडियो"],
        )

    def test_duration_fits(self):
        srt = build_srt("a b c d e f g h", duration=8, max_words=4)
        self.assertIn("00:00:04,000 --> 00:00:08,000", srt)

    def test_empty(self):
        self.assertEqual(build_srt("   "), "")


if __name__ == "__main__":
    unittest.main()
