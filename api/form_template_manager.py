from tinydb import TinyDB, Query
import re
import json

db_path = "api/tinydb_storage/templates.json"
db = TinyDB(db_path)


SUPPORTED_FIELD_TYPES = {"email", "phone", "date", "text"}


def prettify_json(file_path):
    """
    Преобразует JSON файл в читаемый формат с отступами.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)  

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)  

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
    prettify_json(db_path)
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
  
    templates = [
        {
            "name": "User Registration",
            "user_email": "email",
            "user_phone": "phone",
            "date": "date",
            "description": "text"
        },
        {
            "name": "Event Registration",
            "event_name": "text",
            "event_date": "date",
            "event_location": "text",
            "event_contact_email": "email",
            "event_contact_phone": "phone"
        },
        {
            "name": "Product Feedback",
            "product_id": "text",
            "rating": "text",  
            "feedback": "text"
        },
        {
            "name": "Job Application",
            "applicant_name": "text",
            "applicant_email": "email",
            "applicant_phone": "phone",
            "resume": "text"  
        },
        {
            "name": "Customer Support Request",
            "customer_name": "text",
            "issue_description": "text",
            "contact_email": "email",
            "contact_phone": "phone",
            "issue_date": "date"
        }
    ]

    try:
      
        for template in templates:
            add_template(template)
            print(f"Шаблон '{template['name']}' добавлен успешно!")

     
        templates = get_templates()
        print("Список шаблонов:", templates)

    except ValueError as e:
        print(f"Ошибка: {e}")