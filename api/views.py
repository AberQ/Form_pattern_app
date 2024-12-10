
from django.shortcuts import render
from django.http import HttpResponseRedirect

import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tinydb import Query

from .serializers import FormInputSerializer
from .form_template_manager import db  






def determine_field_type(value):
    """
    Определяет тип значения на основе его формата.
    Приоритет проверки: дата -> телефон -> email -> текст.
    """
   
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):  
        return "date"
    
   
    if re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value):  
        return "phone"
    

    if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", value):  
        return "email"
    

    return "text"

def find_matching_template(data):
    """
    Ищет подходящий шаблон в базе данных MongoDB.
    Если шаблон не найден, возвращает None и определяет типы всех полей.
    """
    templates = db['templates'].find()  
    
    for template in templates:
        is_match = True

        for field, value in data.items():
            if field == "name":  
                continue
         
            if field not in template or determine_field_type(value) != template[field]:
                is_match = False
                break

        if is_match:
            return template["name"] 
    
    return None
def get_field_types(data):
    """
    Возвращает объект с именами полей и их определенными типами.
    """
    return {field: determine_field_type(value) for field, value in data.items()}

class GetFormAPIView(APIView):
    """
    API для поиска шаблона по данным формы.
    """
    def post(self, request):
        try:
          
            form_data = request.data  

            if not form_data:
                return Response(
                    {"error": "Данные формы отсутствуют."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

         
            template_name = find_matching_template(form_data)

            if template_name:
                return Response({"template_name": template_name}, status=status.HTTP_200_OK)
            else:
            
                field_types = get_field_types(form_data)
                return Response(field_types, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)