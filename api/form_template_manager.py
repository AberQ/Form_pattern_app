from tinydb import TinyDB, Query
import re

# Путь к файлу базы данных TinyDB
db_path = "api/tinydb_storage/templates.json"
db = TinyDB(db_path)

# Поддерживаемые типы данных
SUPPORTED_FIELD_TYPES = {"email", "phone", "date", "text"}

def validate_template(template):
    """
    Проверка валидности структуры шаблона.
    """
    if not isinstance(template, dict):
        raise ValueError("Шаблон должен быть объектом (dict).")

    if "name" not in template or not isinstance(template["name"], str):
        raise ValueError("Шаблон должен содержать поле 'name' с типом строка.")

    for field, field_type in template.items():
        if field == "name":
            continue
        if not isinstance(field, str):
            raise ValueError(f"Название поля '{field}' должно быть строкой.")
        if field_type not in SUPPORTED_FIELD_TYPES:
            raise ValueError(f"Тип данных '{field_type}' не поддерживается.")
    return True

def add_template(template):
    """
    Добавление нового шаблона в базу данных.
    """
    validate_template(template)
    db.insert(template)

def get_templates():
    """
    Получение всех шаблонов.
    """
    return db.all()

def find_template_by_name(name):
    """
    Поиск шаблона по имени.
    """
    query = Query()
    return db.search(query.name == name)

def delete_template_by_name(name):
    """
    Удаление шаблона по имени.
    """
    query = Query()
    db.remove(query.name == name)

if __name__ == "__main__":
    # Пример шаблона формы
    template = {
        "name": "User Registration",
        "field_name_1": "email",
        "field_name_2": "phone",
        "field_name_3": "date",
        "field_name_4": "text"
    }

    try:
        # Добавление шаблона
        add_template(template)
        print("Шаблон добавлен успешно!")

        # Получение всех шаблонов
        templates = get_templates()
        print("Список шаблонов:", templates)

        # Поиск шаблона
        found_template = find_template_by_name("User Registration")
        print("Найденный шаблон:", found_template)

        # Удаление шаблона
        #delete_template_by_name("User Registration")
        #print("Шаблон удален успешно!")
    except ValueError as e:
        print(f"Ошибка: {e}")
