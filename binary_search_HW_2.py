def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1

        # інакше x присутній на позиції і повертаємо його
        else:
            return iterations, arr[mid]  # знайдено елемент

    # Верхня межа: найменший елемент, який більший або рівний x
    upper_bound = arr[low] if low < len(arr) else None

    # якщо елемент не знайдений
    return iterations, upper_bound


# Тестуємо оновлену функцію
arr = [2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
x = 55
result = binary_search(arr, x)
print(f"Iterations: {result[0]}, Element/Upper Bound: {result[1]}")
