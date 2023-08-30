from django import forms

from .models import STATUS_CHOICE, Loan


CHOICE_INPUT_MAPPING = {
    'text': forms.CharField,
    'number': forms.FloatField,
    'date': forms.DateField,
    'email': forms.EmailField,
    'phone': forms.CharField,
    'boolean': forms.BooleanField,
    'textarea': forms.CharField,
}


class FieldsForm(forms.Form):
    '''
    Recebe os campos para serem criados e valida
    Uso para validar os valores que vêm do front-end
    '''

    def __init__(self, data, fields, *args, **kwargs):
        super(FieldsForm, self).__init__(*args, **kwargs)


        for field in fields:
            self.fields[field.name] = CHOICE_INPUT_MAPPING[field.type](label=field.label, required=field.required, help_text=field.help_text)

        self.data = data
        self.is_bound = True
