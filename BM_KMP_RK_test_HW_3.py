import timeit
from typing import Callable


def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
        return None


def benchmark(func, *args, **kwargs):
    # Збільшення кількості виконань для більш точних результатів
    return timeit.timeit(lambda: func(*args, **kwargs), number=1000)

# Реалізація алгоритму Боєра-Мура 
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

# Реалізація алгоритму Кнута-Морріса-Пратта (KMP)
def kmp_search(pattern, text):
    def compute_lps_array(pattern):
        length = 0
        lps = [0] * len(pattern)
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps_array(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1

# Реалізація алгоритму Рабіна-Карпа
def rabin_karp_search(text, pattern, d=256, q=101):
    M = len(pattern)
    N = len(text)
    p = t = 0  # Хеш значення для шаблону та тексту
    h = 1

    # Обчислення значення h = pow(d, M-1) % q
    for i in range(M-1):
        h = (h * d) % q

    # Обчислення хешу для шаблону та перших M символів тексту
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Слайдинг по тексту
    for i in range(N - M + 1):
        # Перевірка поточного хешу з хешем шаблону
        if p == t:
            # Перевірка символів один за одним
            for j in range(M):
                if text[i+j] != pattern[j]:
                    break
            if j + 1 == M:
                return i  # Шаблон знайдено

        # Обчислення хешу для наступного вікна тексту
        if i < N - M:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + M])) % q
            if t < 0:
                t += q

    return -1  # Шаблон не знайдено


if __name__ == '__main__':
    text1 = read_file('file01.txt')
    text2 = read_file('file02.txt')

    real_pattern1 = "відомих алгоритмів"
    fake_pattern1 = "космічний корабель"
    real_pattern2 = "реалізація методів"
    fake_pattern2 = "привіт всім"

    if text1 is not None:
        results1 = []
        for pattern in (real_pattern1, fake_pattern1):
            # Оновлення порядку аргументів для узгодженості
            time = benchmark(boyer_moore_search, text1, pattern)
            results1.append(('Boyer-Moore', pattern, time))
            time = benchmark(kmp_search, text1, pattern)
            results1.append(('KMP', pattern, time))
            time = benchmark(rabin_karp_search, text1, pattern)
            results1.append(('Rabin-Karp', pattern, time))

    if text2:
        results2 = []
        for pattern in (real_pattern2, fake_pattern2):
            time = benchmark(boyer_moore_search, text2, pattern)
            results2.append(('Boyer-Moore', pattern, time))
            time = benchmark(kmp_search, text2, pattern)
            results2.append(('KMP', pattern, time))
            time = benchmark(rabin_karp_search, text2, pattern)
            results2.append(('Rabin-Karp', pattern, time))

        for results in [results1, results2]:
            title = f"{'Алгоритм':<20} | {'Підрядок':<30} | {'Час виконання, сек'}"
            print("-" * len(title))
            print(title)
            print("-" * len(title))
            for algorithm, pattern, time in results:
                print(f"{algorithm:<20} | {pattern:<30} | {time}")
