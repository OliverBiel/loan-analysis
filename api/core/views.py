from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets, status

from .forms import FieldsForm
from .models import STATUS_CHOICE, Field, Loan
from .serializers import FieldSerializer, LoanSerializer
from rest_framework.decorators import action


class CoreViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get_queryset(self):
        return self.queryset.filter(enabled=True).order_by('order')

    @action(detail=False, methods=['get'])
    def get_uuid(self, request):
        '''
        Retorna o uuid do usuário
        '''
        try:
            uuid = self.request.COOKIES.get('user_uuid')

            if not uuid:
                import uuid
                uuid = uuid.uuid4()

                return Response({'user_uuid': uuid}, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Erro ao obter uuid'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_fields(self, request):
        '''
        Retorna os campos ativos
        '''
        try:
            active_fields = Field.objects.filter(enabled=True).order_by('order')
            response = FieldSerializer(active_fields, many=True)
            response = [{
                'name': field.get('name'),
                'type': field.get('type'),
                'label': field.get('label'),
                'help_text': field.get('help_text'),
                'required': field.get('required'),
            } for field in response.data]

            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Erro ao obter campos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def save_loan(self, request):
        '''
        Recebe os dados do formulário e salva o empréstimo
        Formato:
        {
            "userUUID": str,
            "data": 
                {
                    form_field: Form_field_value
                }
        }

        Salva o campo data como JSON
        Formato:
        { 
            "data": {
                "form_field": Form_field_value,
            },
            "form": [{
                "name": form_field:str,
                "type": form_field_type:str,
                "label": str,
                "required": true/false,
                "help_text": null/str
            }]
        }

        '''
        from .tasks import analyse_loan
        

        try:
            active_fields = Field.objects.filter(enabled=True).order_by('order')
            data = request.data

            form = FieldsForm(data=data['data'], fields=active_fields)
            print(f"Form data: {form.data}")
            print(f"Data: {data}")
            print(f"Fields: {form.fields}")

            if not form.is_valid():
                print(f"Errors: {form.errors}")
                return Response({'error': 'Erro ao validar formulário', 'message': form.errors}, status=status.HTTP_400_BAD_REQUEST)

            uuid = data.get('userUUID')
            data = data.get('data')

            fields_json = [{
                'name': field.name,
                'type': field.type,
                'label': field.label,
                'help_text': field.help_text,
                'required': field.required,
            } for field in active_fields]

            loan = Loan.objects.create(user_uuid=uuid, data={"data": data, "form": fields_json}, status='0')
            
            loan.save()
            analyse_loan.delay(data, loan.id)

            return Response({'success': 'Empréstimo salvo com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Erro ao salvar empréstimo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def get_loans(self, request, uuid):
        '''
        Retorna os empréstimos do usuário
        '''
        try:
            loans = Loan.objects.filter(user_uuid=uuid).order_by('-updated_at')
            response = LoanSerializer(loans, many=True)

            response = [{
                'id': loan.get('id'),
                'status': STATUS_CHOICE[int(loan.get('status'))][1],
                'updated_at': str(loan.get('updated_at')),
            } for loan in response.data]

            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Erro ao obter empréstimos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)