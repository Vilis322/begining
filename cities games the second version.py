import random


def check_validity(city):
    first_valid_cities, second_valid_cities, last_char, first_char = get_valid_cities()

    city = city.title().strip().replace(" ", "-")
    char = city[0].capitalize() if city else None

    if city in used_cities:
        return False

    if city in cities:
        if not used_cities or first_valid_cities and char in last_char or second_valid_cities and char in first_char:
            cities.remove(city)
            used_cities.append(city)
            write_move_to_file("игрока", city)
            return city, cities, used_cities

        return None


def computer_move():
    first_valid_cities, second_valid_cities, last_char, first_char = get_valid_cities()
    valid_cities = first_valid_cities + second_valid_cities

    random_city = random.choice(valid_cities) if valid_cities else random.choice(cities) if not used_cities else None

    if random_city:
        cities.remove(random_city)
        used_cities.append(random_city)
        write_move_to_file("компьютера", random_city)
        print(f"Ход компьютера - {random_city}")
        return random_city, cities, used_cities
    return None


def write_move_to_file(player, move):
    with open("moves.txt", "a", encoding="utf-8") as file_moves:
        file_moves.write(f"\nХод {player} - {move}\n")


def get_valid_cities():
    last_city = used_cities[-1] if used_cities else None
    last_char = last_city[-1].capitalize().strip() if last_city else None
    first_char = last_city[0].capitalize().strip() if last_city else None
    first_valid_cities = [city for city in cities if city.startswith(last_char)] if last_char else []
    second_valid_cities = [city for city in cities if city.startswith(first_char)] if not first_valid_cities and \
                                                                                            first_char else []

    return first_valid_cities, second_valid_cities, last_char, first_char


def game(cities_list, used_cities_list):
    count_tries = 5
    first_move_done = None
    lexical_dict = {1: "осталась одна попытка.", 2: "осталось две попытки.", 3: "осталось три попытки.", 4:
                    "осталось четыре попытки.", 0: "не осталось попыток."}
    computer_move_result = ''

    while count_tries > 0:
        if not first_move_done:
            first_move = random.randint(0, 1)
            if first_move == 0:
                print("Выпала решка. Компьютер ходит первый.")
                computer_move_result = computer_move()
                first_move_done = True
            else:
                print("Выпал орёл. Вы ходите первым.")
                first_move_done = True

        player_city = input("Ваш ход - ")
        player_move = check_validity(player_city)

        if player_move is False:
            count_tries -= 1
            print(f"Такой город уже был назван в текущей игре. У вас {lexical_dict[count_tries]}")
            continue

        if player_move is None:
            count_tries -= 1
            print(f"Такого города не существует. У Вас {lexical_dict[count_tries]}")
            continue

        if player_move:
            computer_move_result = computer_move()

        if computer_move_result is None:
            print("Компьютер не может найти город для своего хода. Вы победили.\nПоздравляю!")
            with open("moves.txt", "a", encoding="utf-8") as file_moves:
                file_moves.write("\nВы победили. Поздравляю!\n")
            break

    if count_tries == 0:
        print("Вы исчерпали свои попытки. Компьютер победил.\nУдачи в последующих играх!")
        with open("moves.txt", "a", encoding="utf-8") as file_moves:
            file_moves.write("\nКомпьютер победил. Удачи в последующих играх!\n")


if __name__ == "__main__":
    with open("cities.txt", "r", encoding="utf-8") as file:
        cities = [line.title().strip().replace(" ", "-") for line in file.read().splitlines()]

    with open("moves.txt", "w", encoding="utf-8") as clean_file:
        pass

    used_cities = []

    print(input("Добро пожаловать в игру 'Города'!\nВы будете играть против компьютера.\nНажмите enter, чтобы узнать "
                "правила игры.\n"))

    print("Первое правило: в игре можно использовать только города России.\nВторое правило: для начала игры нужно "
          "подбросить монетку. Если выпал орёл - первый ход Ваш, если решка - компьютера.\nТретье правило: текущим "
          "ходом должен быть назван город, первая буква в названии которого является последней буквой в названии "
          "предыдущего города.\nЧетвёртое правило: если нет городов, начинающихся на последнюю букву предыдущего города"
          ", необходимо назвать город, начинающийся на первую букву предыдущего города.\nПятое правило: если компьютер "
          "не сможет походить, то Вы победили.\nШестое правило: города не могут повторяться.\nСедьмое правило: у вас "
          "есть 5 попыток.")

    print(input("Нажмите enter, чтобы подбросить монетку."))

    print("\nУдачной игры!")

    game(cities, used_cities)
