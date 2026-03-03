from models.user import User
from models.pet_profile import PetProfile
from models.match_system import MatchSystem
from utils.filters import filter_pets
from utils.data_handler import load_data, save_data

DATA_FILE = "data.json"

def load_from_file(system):
    data = load_data(DATA_FILE)
    #  формат данных:
    # {
    #   "users": [
    #       {
    #           "username": "user1",
    #           "pets": [
    #               {"name": "Rex", "breed": "Labrador", "age": 3, "description": "Friendly dog", "family_history":[], "awards":[]}
    #           ]
    #       }
    #   ]
    # }
    users_data = data.get("users", [])
    for udata in users_data:
        user = User(udata["username"])
        for pdata in udata.get("pets", []):
            pet = PetProfile(
                pdata["name"],
                pdata["breed"],
                pdata["age"],
                pdata["description"]
            )
            for fam in pdata.get("family_history", []):
                pet.add_family_member(fam["relation"], fam["name"], fam["breed"])
            for award in pdata.get("awards", []):
                pet.add_award(award)
            user.add_pet(pet)
        system.add_user(user)

def save_to_file(system):
    data = {"users": []}
    for user in system.all_users:
        user_data = {"username": user.username, "pets": []}
        for pet in user.pets:
            user_data["pets"].append({
                "name": pet.name,
                "breed": pet.breed,
                "age": pet.age,
                "description": pet.description,
                "family_history": pet.family_history,
                "awards": pet.awards
            })
        data["users"].append(user_data)
    save_data(DATA_FILE, data)

def create_user(system):
    username = input("Введите имя пользователя: ")
    user = User(username)
    system.add_user(user)
    print(f"Пользователь {username} успешно создан!")

def add_pet_to_user(system):
    username = input("Введите имя пользователя, к которому нужно добавить питомца: ")
    user = next((u for u in system.all_users if u.username == username), None)
    if not user:
        print("Пользователь не найден!")
        return
    name = input("Имя питомца: ")
    breed = input("Порода питомца: ")
    age = int(input("Возраст питомца: "))
    description = input("Описание питомца: ")
    pet = PetProfile(name, breed, age, description)
    user.add_pet(pet)
    print(f"Питомец {name} добавлен пользователю {username}.")

def view_all_pets(system):
    all_pets = []
    for user in system.all_users:
        all_pets.extend(user.pets)
    if not all_pets:
        print("Нет доступных питомцев.")
        return
    for i, pet in enumerate(all_pets, start=1):
        summary = pet.get_summary()
        print(f"{i}. Имя: {summary['Name']}, Порода: {summary['Breed']}, Возраст: {summary['Age']}, Описание: {summary['Description']}")

def filter_pets_interface(system):
    breed = input("Фильтр по породе (оставьте пустым, если не нужно): ")
    age_input = input("Фильтр по возрастному диапазону, формат min,max (оставьте пустым, если не нужно): ")
    awards_input = input("Фильтр по наградам, через запятую (оставьте пустым, если не нужно): ")

    age_range = None
    if age_input:
        parts = age_input.split(",")
        if len(parts) == 2:
            age_range = (int(parts[0].strip()), int(parts[1].strip()))

    awards = None
    if awards_input:
        awards = [a.strip() for a in awards_input.split(",")]

    all_pets = []
    for user in system.all_users:
        all_pets.extend(user.pets)

    filtered = filter_pets(all_pets, breed=breed if breed else None, age_range=age_range, awards=awards)
    if filtered:
        for pet in filtered:
            print(pet.get_summary())
    else:
        print("Нет питомцев, соответствующих заданным критериям.")

def find_matches_for_user(system):
    username = input("Введите имя пользователя, для которого нужно найти совпадения: ")
    user = next((u for u in system.all_users if u.username == username), None)
    if not user:
        print("Пользователь не найден!")
        return

    matches = system.find_matches(user)
    if not matches:
        print("Совпадений не найдено.")
        return

    print(f"Возможные совпадения для {username}:")
    for pet in matches:
        print(pet.get_summary())

def create_match_between_users(system):
    user1_name = input("Введите имя первого пользователя: ")
    user2_name = input("Введите имя второго пользователя: ")

    user1 = next((u for u in system.all_users if u.username == user1_name), None)
    user2 = next((u for u in system.all_users if u.username == user2_name), None)

    if not user1 or not user2:
        print("Один или оба пользователя не найдены!")
        return

    system.create_match(user1, user2)
    print("Match успешно создано!")

def show_users(system):
    if not system.all_users:
        print("Пользователи не найдены.")
        return
    print("Зарегистрированные пользователи:")
    for user in system.all_users:
        print(f"- {user.username}")

def run_library_system():
    system = MatchSystem()
    load_from_file(system)

    while True:
        print("\nМеню:")
        print("1. Создать пользователя")
        print("2. Добавить питомца пользователю")
        print("3. Просмотреть всех питомцев")
        print("4. Фильтр по питомцам")
        print("5. Найти совпадения для пользователя")
        print("6. Создать совпадение между пользователями")
        print("7. Показать всех пользователей")
        print("8. Сохранить и выйти")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            create_user(system)
        elif choice == "2":
            add_pet_to_user(system)
        elif choice == "3":
            view_all_pets(system)
        elif choice == "4":
            filter_pets_interface(system)
        elif choice == "5":
            find_matches_for_user(system)
        elif choice == "6":
            create_match_between_users(system)
        elif choice == "7":
            show_users(system)
        elif choice == "8":
            save_to_file(system)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неправильный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    run_library_system()
