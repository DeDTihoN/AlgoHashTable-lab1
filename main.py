import random
import string
from collections import defaultdict

import Hash
import HashTable
import timeit
import unittest


def generate_random_string(max_len=15):
    """Генерує випадковий рядок довжиною до max_len."""
    length = random.randint(1, max_len)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_test(num_commands=100, prob_remove=0.1, prob_query=0.45, max_len=15):
    """Генерує рандомні тести для хеш-таблиці."""
    test_cases = []
    added_strings = []  # Список доданих рядків

    for _ in range(num_commands):
        rand_num = random.random()

        if rand_num < prob_remove and added_strings:
            s = random.choice(added_strings)
            test_cases.append(f"- {s}")
            added_strings.remove(s)

        elif rand_num < prob_remove + prob_query and added_strings:
            s = random.choice(added_strings)
            test_cases.append(f"? {s}")

        else:
            s = generate_random_string(max_len)
            test_cases.append(f"+ {s}")
            added_strings.append(s)

    test_cases.append("#")
    return test_cases


def save_test_to_file(test_cases, filename):
    """Зберігає тест-кейси в файл."""
    with open(filename, 'w') as f:
        f.write('\n'.join(test_cases))


def read_test_from_file(filename):
    """Зчитує тест-кейси з файлу."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def run_test(test_cases, hash_table):
    """Читає тести та виконує їх на хеш-таблиці."""
    results = []

    for line in test_cases:
        if line == "#":
            break
        command, s = line.split()

        if command == "+":
            hash_table.add(s)
        elif command == "-":
            hash_table.remove(s)
        elif command == "?":
            contains = hash_table.contains(s)
            result = f"Contains {s}: {'Yes' if contains else 'No'}"
            results.append(result)

    groups = hash_table.get_groups()
    group_results = []

    for group in groups:
        group_str = f"String: {group[0]}, Count: {group[1]}"
        group_results.append(group_str)

    return results, group_results


def validate_test_results(test_cases):
    """Валідує результати з урахуванням кількості появ елементів."""
    element_count = defaultdict(int)  # Використовуємо словник для підрахунку кількості кожного елементу
    validation_results = []

    for line in test_cases:
        if line == "#":
            break
        command, s = line.split()

        if command == "+":
            element_count[s] += 1  # Збільшуємо лічильник для рядка
        elif command == "-" and element_count[s] > 0:
            element_count[s] -= 1  # Зменшуємо лічильник, але не видаляємо при нулі
        elif command == "?":
            result = f"Contains {s}: {'Yes' if element_count[s] > 0 else 'No'}"
            validation_results.append(result)

    validation_groups = {}
    for s, count in element_count.items():
        if count > 0:
            validation_groups[s] = count

    group_results = [f"String: {k}, Count: {v}" for k, v in validation_groups.items()]
    return validation_results, group_results


def compare_results(test_results, validation_results):
    """Порівнює результати тестування з валідаційними результатами."""
    test_contains, test_groups = test_results
    valid_contains, valid_groups = validation_results

    test_groups.sort()
    valid_groups.sort()

    if test_contains != valid_contains:
        return False, f"❌ Помилка в результатах пошуку: {test_contains} != {valid_contains}"

    if test_groups != valid_groups:
        return False, f"❌ Помилка в групах елементів: {test_groups} != {valid_groups}"

    return True, "✅ Усі результати правильні"


def generate_and_save_test(filename, num_commands=100):
    """Генерує тест, зберігає його у файл."""
    test_cases = generate_test(num_commands)
    save_test_to_file(test_cases, filename)


def read_and_validate_test(filename, hash_table):
    """Зчитує тест з файлу, виконує та порівнює результати з валідованими."""
    test_cases = read_test_from_file(filename)

    test_results = run_test(test_cases, hash_table)
    validation_results = validate_test_results(test_cases)

    return compare_results(test_results, validation_results)


def read_and_run_test(filename, hash_table):
    """Зчитує тест з файлу та виконує його."""
    test_cases = read_test_from_file(filename)
    test_results = run_test(test_cases, hash_table)
    return test_results


# Клас для тестів та бенчмарків
class TestHashTable(unittest.TestCase):

    def test_basic_functionality(self):
        """Тестує базові функції хеш-таблиці на простому прикладі."""
        hasher = Hash.Hash()
        ht = HashTable.HashTable(hasher=hasher)

        commands = ["+ abc", "+ xyz", "? abc", "? xyz", "- abc", "? abc", "#"]
        test_results = run_test(commands, ht)
        validation_results = validate_test_results(commands)

        result, message = compare_results(test_results, validation_results)
        self.assertTrue(result, message)

    def test_basic_second(self):
        """Тестує базові функції хеш-таблиці на простому прикладі."""

        hasher = Hash.Hash()
        ht = HashTable.HashTable(hasher=hasher)

        commands = ["+ a", "+ a", "+ a", "? a", "+ a", "- a", "? a", "#"]
        test_results = run_test(commands, ht)
        validation_results = validate_test_results(commands)

        result, message = compare_results(test_results, validation_results)
        self.assertTrue(result, message)

    def test_with_generated_test(self):
        """Тестує хеш-таблицю на згенерованому тесті."""
        filename = "test_generated.txt"
        hasher = Hash.Hash()
        ht = HashTable.HashTable(hasher=hasher)

        generate_and_save_test(filename, num_commands=100)

        result, message = read_and_validate_test(filename, ht)
        self.assertTrue(result, message)

    def test_generated_test_bigger(self):
        """Тестує хеш-таблицю на згенерованому більшому тесті."""
        filename = "test_generated_big.txt"
        hasher = Hash.Hash()
        ht = HashTable.HashTable(hasher=hasher)

        generate_and_save_test(filename, num_commands=100000)

        result, message = read_and_validate_test(filename, ht)
        self.assertTrue(result, message)

    def test_benchmark(self):
        """Виконує бенчмарк для хеш-таблиці."""
        hasher = Hash.Hash()
        ht = HashTable.HashTable(hasher=hasher)

        def benchmark():
            filename = "test_benchmark.txt"
            # generate_and_save_test(filename, num_commands=1000000)
            read_and_run_test(filename, ht)

        # Вимірюємо час виконання
        time_taken = timeit.timeit(benchmark, number=1)
        print(f"Benchmark time: {time_taken:.4f} seconds")


if __name__ == '__main__':
    unittest.main(verbosity=2)
