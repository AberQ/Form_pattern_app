from django import forms
from tinydb import TinyDB, Query
from django.core.validators import RegexValidator

# TinyDB: путь к базе данных
db_path = "api/tinydb_storage/templates.json"
db = TinyDB(db_path)

class DynamicForm(forms.Form):
    """
    Генерация формы на основе шаблона.
    """
    @classmethod
    def from_template(cls, template_name):
        # Поиск шаблона в базе
        query = Query()
        template = db.get(query.name == template_name)

        if not template:
            raise ValueError(f"Шаблон с именем '{template_name}' не найден.")

        # Создание динамического класса формы
        form_fields = {}
        for field, field_type in template.items():
            if field == "name":
                continue  # Поле 'name' не добавляется как поле формы

            if field_type == "email":
                form_fields[field] = forms.EmailField(label=field.capitalize())
            elif field_type == "phone":
                phone_validator = RegexValidator(
                    regex=r'^\+?1?\d{9,15}$',
                    message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
                )
                form_fields[field] = forms.CharField(
                    label=field.capitalize(),
                    max_length=15,
                    validators=[phone_validator],
                )
            elif field_type == "date":
                form_fields[field] = forms.DateField(label=field.capitalize(), widget=forms.DateInput(attrs={'type': 'date'}))
            elif field_type == "text":
                form_fields[field] = forms.CharField(label=field.capitalize(), widget=forms.Textarea)

        return type("DynamicForm", (cls,), form_fields)
