from api.form_template_manager import add_template

def create_test_data():
    """
    Создает тестовые данные и добавляет их в базу данных.
    """
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

    for template in templates:
        try:
            add_template(template)
            print(f"Шаблон '{template['name']}' добавлен успешно!")
        except ValueError as e:
            print(f"Ошибка при добавлении шаблона '{template['name']}': {e}")


if __name__ == "__main__":
    create_test_data()
