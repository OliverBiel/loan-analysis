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

class LoanForm(forms.ModelForm):
    '''
    Formulário para o modelo Loan no Admin
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.data and self.instance.status in ['2', '0']:  # Se o status for 'Em análise' ou 'Reprovado':
            self.fields['avaliation'].widget.attrs['readonly'] = True
            self.fields['avaliation'].widget.attrs['disabled'] = True
            self.fields['status'].widget.attrs['readonly'] = True
            self.fields['status'].widget.attrs['disabled'] = True

    class Meta:
        model = Loan
        exclude = ('user_uuid', 'created_at', 'updated_at', 'data')

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
