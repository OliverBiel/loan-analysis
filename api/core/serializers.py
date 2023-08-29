from rest_framework.serializers import ModelSerializer
from .models import Field, Loan


class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


