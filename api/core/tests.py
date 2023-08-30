from django.test import TestCase
from .models import Field


class LoanTest(TestCase):
    def setUp(self):
        self.field1 = Field.objects.create(
            name='field',
            type='text',
            label='Field',
            required=True,
            help_text='Field help text',
            enabled=True,
            order=1
        )

        self.field2 = Field.objects.create(
            name='field2',
            type='text',
            label='Field2',
            required=False,
            help_text='Field2 help text',
            enabled=True,
            order=2
        )

        self.disabled_field = Field.objects.create(
            name='disabled_field',
            type='text',
            label='Disabled Field',
            required=False,
            help_text='Disabled Field help text',
            enabled=False,
            order=3
        )

        self.test_userUUID = str(self.client.get('/uuid/').data['user_uuid'])

    def test_fields(self):
        field1 = Field.objects.get(name='field')
        field2 = Field.objects.get(name='field2')
        disabled_field = Field.objects.get(name='disabled_field')

        self.assertEqual(field1.name, 'field')
        self.assertEqual(field1.type, 'text')
        self.assertEqual(field1.label, 'Field')
        self.assertEqual(field1.required, True)
        self.assertEqual(field1.help_text, 'Field help text')
        self.assertEqual(field1.enabled, True)
        self.assertEqual(field1.order, 1)

        self.assertEqual(field2.name, 'field2')
        self.assertEqual(field2.type, 'text')
        self.assertEqual(field2.label, 'Field2')
        self.assertEqual(field2.required, False)
        self.assertEqual(field2.help_text, 'Field2 help text')
        self.assertEqual(field2.enabled, True)
        self.assertEqual(field2.order, 2)

        self.assertEqual(disabled_field.name, 'disabled_field')
        self.assertEqual(disabled_field.type, 'text')
        self.assertEqual(disabled_field.label, 'Disabled Field')
        self.assertEqual(disabled_field.required, False)
        self.assertEqual(disabled_field.help_text, 'Disabled Field help text')
        self.assertEqual(disabled_field.enabled, False)
        self.assertEqual(disabled_field.order, 3)

    def test_get_fields_view(self):
        response = self.client.get('/fields/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'field')
        self.assertEqual(response.data[1]['name'], 'field2')
    
    def test_get_uuid_view(self):
        response = self.client.get('/uuid/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['user_uuid'])
    
    def test_save_loan_view(self):
        field1 = self.field1.name
        field2 = self.field2.name
        disabled_field = self.disabled_field.name

        req_body = {
            'userUUID': self.test_userUUID,
            'data': {
                field1: 'value',
                field2: 'value2'
            }
        }

        response = self.client.post('/loan/', data=req_body, format='json', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

        req_body['data'][disabled_field] = 'value'

        error_response = self.client.post('/loan/', data=req_body, format='json', content_type='application/json')

        self.assertEqual(error_response.status_code, 400)