from random import randint


def generate_invite_code(id=2):
    """Тестовая функция генерации инвайт кода."""
    alphabet = "abcdefgABCDEFGhijklstuvwxyzHIJKLMNOPQRSmnopqrTUVWXYZ"
    code = ""

    numbers = [0, 0, 0, 0, 0, 0]

    for index in range(6):
        numbers[index] = randint(1, 53)

    for index in range(6):
        code += str(f"{alphabet[numbers[index]]}")
    numbers = map(lambda number: number * id, numbers)


generate_invite_code()
