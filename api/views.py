
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DynamicForm
import re
def dynamic_form_view(request, template_name):
    """
    Представление для отображения динамической формы.
    """
    try:
        FormClass = DynamicForm.from_template(template_name)
    except ValueError as e:
        return render(request, "error.html", {"error": str(e)})

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            # Обработка данных формы
            print("Данные формы:", form.cleaned_data)
            return HttpResponseRedirect("/success/")  # Перенаправление на страницу успеха
    else:
        form = FormClass()

    return render(request, "dynamic_form.html", {"form": form, "template_name": template_name})




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tinydb import Query

from .serializers import FormInputSerializer
from .form_template_manager import db  # Подключаем вашу TinyDB

def determine_field_type(value):
    """
    Определяет тип значения на основе его формата.
    """
    if re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value):  # Формат телефона: +7 xxx xxx xx xx
        return "phone"
    elif re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", value):  # Email
        return "email"
    elif re.match(r"^\d{4}-\d{2}-\d{2}$", value):  # Дата в формате YYYY-MM-DD
        return "date"
    else:
        return "text"


def find_matching_template(data):
    """
    Ищет подходящий шаблон в базе данных TinyDB.
    """
    templates = db.all()  # Получение всех шаблонов
    for template in templates:
        is_match = True

        # Проверяем только поля, переданные в запросе
        for field, value in data.items():
            if field == "name":  # Игнорируем поле "name"
                continue
            # Если поля нет в шаблоне или тип значения не совпадает, шаблон не подходит
            if field not in template or determine_field_type(value) != template[field]:
                is_match = False
                break

        if is_match:
            return template["name"]  # Возвращаем имя подходящего шаблона
    return None

class GetFormAPIView(APIView):
    """
    API для поиска шаблона по данным формы.
    """
    def post(self, request):
        try:
            # Получение данных из POST-запроса
            form_data = request.data  # DRF автоматически парсит JSON/форму

            if not form_data:
                return Response(
                    {"error": "Данные формы отсутствуют."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Поиск подходящего шаблона
            template_name = find_matching_template(form_data)

            if template_name:
                return Response({"template_name": template_name}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Шаблон не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)