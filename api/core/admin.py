from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse

from .forms import LoanForm
from .models import Field, Loan


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'label', 'help_text', 'required', 'order', 'enabled')
    list_filter = ('type', 'required', 'enabled')
    search_fields = ('name', 'label', 'help_text')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_filter = ('status',)
    search_fields = ('user_uuid',)
    form = LoanForm
    change_form_template = 'change_form.html'

    
    def change_view(self, request: HttpRequest, object_id: str, form_url: str="", extra_context=None) -> HttpResponse:
        # Obtenho os campos do formulário pelo valor do campo data e adiciono ao contexto
        extra_context = extra_context or {}

        data = Loan.objects.filter(id=object_id).values('data').first()
        data = data.get('data') if data else None

        if data:
            fields = data.get('form')
            for field in fields:
                field['value'] = data['data'][field['name']]
            extra_context['my_fields'] = fields

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

