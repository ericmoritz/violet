import unittest
from violet import is_type, passes, cast


class TestIsType(unittest.TestCase):
    def test_type(self):
        self.assertEqual("Hi", is_type(str)("Hi"))
        self.assertEqual(1, is_type(int)(1))
        self.assertEqual(1.0, is_type(float)(1.0))
        self.assertEqual([], is_type(list)([]))
        self.assertEqual({1}, is_type(set)({1}))
        self.assertEqual({"foo": "bar"}, is_type(dict)({"foo":"bar"}))

        self.assertRaises(TypeError, is_type(int), 1.0)

    def test_constant(self):
        self.assertEqual(1, is_type(1)(1))

    def test_list(self):
        validator = is_type([int,str])
        self.assertEqual([1,2], validator([1,2]))
        self.assertEqual(["foo"], validator(["foo"]))
        self.assertRaises(TypeError, validator, "foo")
        self.assertRaises(TypeError, validator, [1.0])

    def test_list_composite(self):
        validator = is_type([cast(int) & passes(lambda x: x >= 10)])
        self.assertEqual([10, 11, 12],
                         validator([10,11,12]))

        self.assertRaises(ValueError, validator, ["foo"])
        self.assertRaises(AssertionError, validator, [1])


    def test_set(self):
        self.assertEqual({1, 2}, is_type({int})({1,2}))

    def test_set_composite(self):
        validator = is_type({cast(int) & passes(lambda x: x >= 10)})
        self.assertEqual({10, 11, 12},
                         validator({10,11,12}))

        self.assertRaises(ValueError, validator, {"foo"})
        self.assertRaises(AssertionError, validator, {1})

    def test_dict(self):
        validator = is_type({
                "name": str,
                "age": int,
                })
        self.assertEqual({"name": "Eric", "age": 32},
                         validator({"name": "Eric",
                                    "age": 32}))
    def test_complex(self):
        validator = is_type(
            [
                {
                    "name": is_type(str) & passes(len),
                    "age": cast(int) & passes(lambda x: 18 <= x <= 99),
                    "sex": cast(str.lower) & passes(lambda s: s in ["male", "female"])
                    }
                ])
            
        data = [{'name': 'Sue', 'age': '28', 'sex': 'FEMALE'},
                {'name': 'Sam', 'age': '42', 'sex': 'Male'},
                {'name': 'Sacha', 'age': '20', 'sex': 'Male'}]

        self.assertEqual(
            [{'name': 'Sue', 'age': 28, 'sex': 'female'},
             {'name': 'Sam', 'age': 42, 'sex': 'male'},
             {'name': 'Sacha', 'age': 20, 'sex': 'male'}],
            validator(data))


class TestPasses(unittest.TestCase):
    def test(self):
        self.assertEqual([1], passes(len)([1]))
        self.assertRaises(AssertionError, passes(len), [])


class TestCastAs(unittest.TestCase):
    def test(self):
        self.assertEqual(1, cast(int)("1"))


class TestAnd(unittest.TestCase):
    def test(self):
        validator = cast(int) & is_type(int)
        self.assertEqual(1, validator("1"))

        self.assertRaises(ValueError, validator, "monkey")


class TestOR(unittest.TestCase):
    def test(self):
        validator = is_type(int) | is_type(str)

        self.assertEqual(1, validator(1))
        self.assertEqual("monkey", validator("monkey"))
        
        self.assertRaises(TypeError, validator, 1.0)



