
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

class GetFormView(APIView):
    def post(self, request):
        # Входные данные
        input_fields = request.data
        if not isinstance(input_fields, dict):
            return Response({"error": "Invalid data format. Expected a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

        # Загружаем шаблоны из TinyDB
        templates = db.all()

        for template in templates:
            # Извлекаем поля шаблона, исключая "name"
            template_fields = {k: v for k, v in template.items() if k != "name"}

            # Проверяем, что все поля шаблона есть в input_fields с совпадающими типами
            if all(field in input_fields and input_fields[field] == field_type
                   for field, field_type in template_fields.items()):
                return Response({"template_name": template["name"]}, status=status.HTTP_200_OK)

        return Response({"error": "No matching template found"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def validate_type(value, expected_type):
        """
        Проверяет, соответствует ли тип значения ожидаемому типу.
        """
        type_map = {
            "email": lambda v: isinstance(v, str) and "@" in v,
            "phone": lambda v: isinstance(v, str) and v.isdigit(),
            "date": lambda v: isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v),
            "text": lambda v: isinstance(v, str)
        }
        return type_map.get(expected_type, lambda _: False)(value)
