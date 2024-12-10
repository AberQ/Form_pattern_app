import requests


BASE_URL = "http://127.0.0.1:8000/get_form/"

# Запросы с ожидаемым кодом 200 (положительные результаты)
positive_tests = [
    {"user_email": "test@example.com", "user_phone": "+7 923 456 78 90", "date": "2024-12-10", "description": "Testing"},
    {"event_name": "Party", "event_date": "2024-12-20", "event_location": "City Hall", "event_contact_email": "party@events.com"},
    {"product_id": "12345", "rating": "5", "feedback": "Great product!"},
]

# Запросы с ожидаемым кодом 404 (отрицательные результаты)
negative_tests = [
    {"user_email": "invalid_email", "user_phone": "923 456 78 90", "date": "invalid_date", "description": "Testing"},
    {"applicant_name": "John Doe", "applicant_phone": "12345678", "resume": "Some text without email"},
    {"customer_name": "Alice", "issue_description": "Broken product"},
]

def send_test_request(data, expected_status):
    """
    Отправляет запрос на API и проверяет код ответа.
    """
    print(f"Отправка данных: {data}")
    response = requests.post(BASE_URL, data=data)

    if response.status_code == expected_status:
        print(f"Ожидаемый код {expected_status}. Ответ: {response.json()}")
    else:
        print(f"ОШИБКА! Ожидался код {expected_status}, но получен {response.status_code}. Тело ответа: {response.text}")
    print("-" * 50)

if __name__ == "__main__":

    print("Запросы с кодом 200:")
    for test_data in positive_tests:
        send_test_request(test_data, expected_status=200)

   
    print("Запросы с кодом 404:")
    for test_data in negative_tests:
        send_test_request(test_data, expected_status=404)
