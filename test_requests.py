import requests

# URL вашего API
url = "http://127.0.0.1:8000/get_form/"

# Тестовые данные для отправки
test_data = [
    {
        "user_email": "test@example.com",
        "user_phone": "+7 923 456 78 90",
        "date": "2024-12-10",
        "description": "Testing"
    },
    {
        "event_name": "Tech Conference 2024",
        "event_date": "2024-12-15",
        "event_location": "New York",
        "event_contact_email": "contact@techconf.com",
        "event_contact_phone": "+7 123 456 78 90"
    },
    {
        "product_id": "12345",
        "rating": "5",
        "feedback": "Great product!"
    },
    {
        "applicant_name": "John Doe",
        "email": "john.doe@example.com",
        "applicant_phone": "+7 900 123 45 67",
        "resume": "This is my resume."
    },
    {
        "customer_name": "Jane Smith",
        "issue_description": "The product arrived damaged.",
        "contact_email": "jane.smith@example.com",
        "contact_phone": "+7 912 345 67 89",
        "issue_date": "2024-12-09"
    }
]

# Функция для отправки тестового запроса
def send_test_request(data):
    response = requests.post(url, data=data)
    print(f"Запрос: {data}")
    print(f"Ответ: {response.json()}")
    print("-" * 40)

# Отправка тестовых запросов
for data in test_data:
    send_test_request(data)
