import Hash


class Node:
    def __init__(self, value):
        self.value = value
        self.count = 1  # Лічильник появ елемента
        self.next = None


class HashTable:
    DEFAULT_LEN = int(1e5)  # Default length if not provided

    def __init__(self, Len: int = None, hasher: Hash = None):
        self.Len = Len if Len is not None else self.DEFAULT_LEN
        self.table = [None] * self.Len
        self.hasher = hasher if hasher is not None else Hash.Hash()

    def _get_index(self, s: str):
        hash_value = self.hasher.compute_hash(s)
        return hash_value % self.Len

    def add(self, s: str):
        index = self._get_index(s)
        current = self.table[index]

        # Шукаємо, чи є вже такий елемент
        while current:
            if current.value == s:
                current.count += 1  # Якщо елемент знайдено, збільшуємо лічильник
                return
            current = current.next

        # Якщо елемент не знайдено, додаємо новий
        new_node = Node(s)
        new_node.next = self.table[index]
        self.table[index] = new_node

    def remove(self, s: str):
        index = self._get_index(s)
        prev = None
        current = self.table[index]

        while current:
            if current.value == s:
                if current.count > 1:
                    current.count -= 1  # Зменшуємо лічильник, але не видаляємо елемент
                else:
                    # Видаляємо елемент, якщо лічильник дорівнює 1
                    if prev:
                        prev.next = current.next
                    else:
                        self.table[index] = current.next
                return True
            prev = current
            current = current.next
        return False

    def contains(self, s: str):
        index = self._get_index(s)
        current = self.table[index]

        while current:
            if current.value == s:
                return True
            current = current.next
        return False

    def get_groups(self):
        """Returns pairs of strings and the number of times they appear in the hash table."""
        groups = []

        # Проходимо по кожній комірці хеш-таблиці
        for i in range(self.Len):
            current = self.table[i]

            # Переходимо по зв'язаному списку комірки
            while current:
                groups.append([current.value, current.count])  # Додаємо елемент та його лічильник
                current = current.next

        return groups
