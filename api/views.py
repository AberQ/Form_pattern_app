
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DynamicForm

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
