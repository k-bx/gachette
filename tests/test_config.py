import unittest

from gachette.lib.utils import expand_dotted_keys, dict_tuple_dotted, deep_merge


class DottedTransformTest(unittest.TestCase):
    def test_simple(self):
        self._test("foo", "bar", {"foo": "bar"})
        self._test("foo.faa", "bar", {"foo": {"faa": "bar"}})
        self._test("foo.faa.bri", "bar", {"foo": {"faa": {"bri": "bar"}}})

    def _test(self, k, v, expected):
        result = dict_tuple_dotted(k, v)
        self.assertEqual(result,
                    expected,
                    "not expected: %s" % result)


class DeepMergeTest(unittest.TestCase):
    def test_simple(self):
        self._test({"foo": "bor"},
                    {"faa": "bar" },
                    {"faa": "bar", "foo": "bor"})
        self._test({"foo": "bor"},
                    {"foo": "bar" },
                    {"foo": "bor"})
        self._test({"foo": {"lol": "bor"}},
                    {"foo": {"lal": "bar"} },
                    {"foo": {"lol": "bor", "lal": "bar"}})
        self._test({"aa": "bb", "foo": {"lol": "bor"}},
                    {"foo": {"lal": "bar"} },
                    {"aa": "bb", "foo": {"lol": "bor", "lal": "bar"}})

    def _test(self, a, b, expected):
        result = deep_merge(a, b)
        self.assertEqual(result,
            expected,
            "not expected: %s" % result)

class ExpandDottedTest(unittest.TestCase):
    def test_simple(self):
        self._test({"foo": "bor", "faa": "bar" },
                    {"faa": "bar", "foo": "bor"})
        self._test({"foo": "bor"},
                    {"foo": "bor"})
        self._test({"foo.lol": "bor", "foo.lal": "bar"},
                    {"foo": {"lol": "bor", "lal": "bar"}})
        self._test({"aa": "bb", "foo.lol": "bor", "foo.lal": "bar"},
                    {"aa": "bb", "foo": {"lol": "bor", "lal": "bar"}})

    def _test(self, array, expected):
        result = expand_dotted_keys(array)
        self.assertEqual(result,
            expected,
            "not expected: %s" % result)
