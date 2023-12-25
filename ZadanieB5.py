field = [[" "] * 3 for i in range(3)]

def playing_field():
    print(f"  | 0 | 1 | 2 |")
    print("---------------")
    for i in range(3):
        row_info = " | ".join(field[i])
        print(f"{i} | {row_info} |")
        print("---------------")
    return " "

def check_win():
    for j in range(3):
        list = []
        for k in range(3):
            list.append(field[j][k])
            if list == ["X", "X", "X"]:
                print("Крестики винс!")
                return True
            elif list == ["0", "0", "0"]:
                print("Нолики винс!")
                return True

    for j in range(3):
        list = []
        for k in range(3):
            list.append(field[k][j])
            if list == ["X", "X", "X"]:
                print("Крестики винс!")
                return True
            elif list == ["0", "0", "0"]:
                print("Нолики винс!")
                return True

    list = []
    for j in range(3):
        list.append(field[j][2 - j])
        if list == ["X", "X", "X"]:
            print("Крестики винс!")
            return True
        elif list == ["0", "0", "0"]:
            print("Нолики винс!")
            return True

    list = []
    for j in range(3):
        list.append(field[j][j])
        if list == ["X", "X", "X"]:
            print("Крестики винс!")
            return True
        elif list == ["0", "0", "0"]:
            print("Нолики винс!")
            return True

def ask():
    num = 0
    while True:
        cords = input("Введите числа:").split()

        if len(cords) != 2:
            print("Введите обе координаты!")
            continue

        x, y = cords
        if not x.isdigit() or not y.isdigit():
            print("Введите числа!")
            continue

        x, y = int(x), int(y)
        if x < 0 or x > 2 or y < 0 or y > 2:
            print("Числа не в диапозоне!")
            continue

        if field[x][y] != " ":
            print("Клетка занята!")
            continue

        num += 1

        if num % 2 == 1:
            field[x][y] = "X"
            playing_field()
            if check_win():
                break
            elif num == 9:
                print("Ничья!")
                break
            else:
                print("Следующий ход за ноликом")
                continue

        if num % 2 != 1:
            field[x][y] = "0"
            playing_field()
            if check_win():
                break
            elif num == 9:
                print("Ничья!")
                break
            else:
                print("Следующий ход за крестиком")
                continue

def Start():
    print("Приветствую! \n"
          "Игра крестики-нолики \n"
          "--- \n"
          "Формат ввода: x y \n"
          "x - номер строки \n"
          "y - номер столбца \n"
          " \n")
    print(f"{playing_field()}")
    print("Первым ходит крестик")
    ask()
    input("Введите что угодно для выхода:")


Start()

