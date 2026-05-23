import string
import unittest


# Выносим логику генерации для независимого тестирования
def core_generate_password(length, use_digits, use_letters, use_specials):
    if length < 4 or length > 32:
        raise ValueError("Некорректная длина")

    chars = ""
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_specials:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

    if not chars:
        raise ValueError("Не выбраны символы")

    import random

    return "".join(random.choice(chars) for _ in range(length))


class TestPasswordGenerator(unittest.TestCase):

    # 1. Позитивные тесты
    def test_positive_standard_generation(self):
        pwd = core_generate_password(12, True, True, True)
        self.assertEqual(len(pwd), 12)

    def test_positive_letters_only(self):
        pwd = core_generate_password(10, False, True, False)
        self.assertTrue(pwd.isalpha())

    # 2. Граничные значения
    def test_boundary_min_length(self):
        pwd = core_generate_password(4, True, True, True)
        self.assertEqual(len(pwd), 4)

    def test_boundary_max_length(self):
        pwd = core_generate_password(32, True, True, True)
        self.assertEqual(len(pwd), 32)

    # 3. Негативные сценарии
    def test_negative_too_short(self):
        with self.assertRaises(ValueError):
            core_generate_password(3, True, True, True)

    def test_negative_too_long(self):
        with self.assertRaises(ValueError):
            core_generate_password(33, True, True, True)

    def test_negative_no_options_selected(self):
        with self.assertRaises(ValueError):
            core_generate_password(10, False, False, False)


if __name__ == "__main__":
    unittest.main()
