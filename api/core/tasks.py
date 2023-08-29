from celery import shared_task
import requests

from .models import Loan


@shared_task
def analyse_loan(data, id):
    API_URL = r"https://loan-processor.digitalsys.com.br/api/v1/loan/"
    RESPONSE_MAPPING = {
        True: "1",
        False: "2"
    }

    re_body = {
        "document": data,
        "name": str(id)
    }

    response = requests.post(API_URL, json=re_body)

    try:
        obj = Loan.objects.get(id=id)
        status = RESPONSE_MAPPING.get(response.json().get('approved'))
        obj.status = status

        obj.save()
        
    except Exception as e:
        print('Erro ao atualizar status do empréstimo')
        print(e)