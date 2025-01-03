from pymongo import MongoClient
import json


client = MongoClient('mongo', 27017)
db = client["my_database"]  
collection = db["templates"]  

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
    Добавление нового шаблона в MongoDB с проверкой на уникальность имени.
    """
    validate_template(template)

   
    if collection.find_one({"name": template["name"]}):  
        print(f"Шаблон с именем '{template['name']}' уже существует. Пропускаем добавление.")
        return
    
    
    collection.insert_one(template)
    print(f"Шаблон '{template['name']}' добавлен успешно!")

def get_templates():
    """
    Получение всех шаблонов из MongoDB.
    """
    templates = list(collection.find({}, {"_id": 0}))  
    return templates

def find_template_by_name(name):
    """
    Поиск шаблона по имени.
    """
    template = collection.find_one({"name": name}, {"_id": 0})
    if not template:
        print(f"Шаблон с именем '{name}' не найден.")
    return template

def delete_template_by_name(name):
    """
    Удаление шаблона по имени.
    """
    result = collection.delete_one({"name": name})
    if result.deleted_count == 0:
        print(f"Шаблон с именем '{name}' не найден.")
    else:
        print(f"Шаблон с именем '{name}' успешно удален.")

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

        
        all_templates = get_templates()
        print("Список шаблонов:", json.dumps(all_templates, indent=4, ensure_ascii=False))

       
        template = find_template_by_name("User Registration")
        print("Найденный шаблон:", template)

     
        delete_template_by_name("Job Application")

    except ValueError as e:
        print(f"Ошибка: {e}")
