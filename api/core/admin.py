from typing import Any, Optional, Sequence
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.admin.decorators import action
from datetime import datetime

from .models import STATUS_CHOICE, Field, Loan


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'label', 'help_text', 'required', 'order', 'enabled')
    list_filter = ('type', 'required', 'enabled')
    search_fields = ('name', 'label', 'help_text')

    @action(description='Enable selected fields')
    def enable_fields(self, request: HttpRequest, queryset: Sequence[Field]) -> None:
        queryset.update(enabled=True)

    @action(description='Disable selected fields')
    def disable_fields(self, request: HttpRequest, queryset: Sequence[Field]) -> None:
        queryset.update(enabled=False)
    
    actions = ['enable_fields', 'disable_fields']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_filter = ('status',)
    search_fields = ('user_uuid',)
    exclude = ['data']
    change_form_template = 'change_form.html'

    
    def change_view(self, request: HttpRequest, object_id: str, form_url: str="", extra_context=None) -> HttpResponse:
        # Obtenho os campos do formulário pelo valor do campo data e adiciono ao contexto
        extra_context = extra_context or {}

        data = Loan.objects.filter(id=object_id).values('data').first()
        data = data.get('data') if data else None

        if data:
            fields = data.get('form')
            for field in fields:
                field['value'] = data['data'][field['name']] if field['type'] != 'date' else datetime.strptime(data['data'][field['name']], '%Y-%m-%d').strftime('%d/%m/%Y')
            extra_context['my_fields'] = fields

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj is not None and (obj.status == STATUS_CHOICE[0][0] or obj.status == STATUS_CHOICE[2][0]):
            return False
    
        else:
            return super().has_change_permission(request, obj)
        