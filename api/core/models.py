from typing import Iterable, Optional
from django.db import models
import uuid


TYPES_CHOICES = (
    ('text', 'Texto'),
    ('number', 'Número'),
    ('date', 'Data'),
    ('email', 'E-mail'),
    ('phone', 'Telefone'),
    ('textarea', 'Área de texto'),
)

STATUS_CHOICE = (
    ('0', 'Em Análise'),
    ('1', 'Pré-Aprovado'),
    ('2', 'Reprovado'),
    ('3', 'Aprovado')
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Field(BaseModel):     # Model para cada um dos campos, para montar o form eu obtenho todos os objetos dessa model que estejam ativos (enabled)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    type = models.CharField(max_length=255, null=False, blank=False, choices=TYPES_CHOICES)
    label = models.CharField(max_length=255, null=False, blank=False)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    required = models.BooleanField(default=False, null=False, blank=False)
    order = models.IntegerField(default=0, null=False, blank=False)
    enabled = models.BooleanField(default=False, null=False, blank=False, help_text="Indica se o campo estará presente no formulário de empréstimo")

    def __str__(self):
        return self.name

class Loan(BaseModel):
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False) # Esse valor será gerado pelo endpoint /uuid/ e estará como cookie no frontend
    data = models.JSONField(null=False, blank=False)
    status = models.CharField(max_length=1, null=False, blank=False, choices=STATUS_CHOICE)
    avaliation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | Usuário: {self.user_uuid}"