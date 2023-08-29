import { Component, Input, OnInit, OnChanges } from '@angular/core';
import { Field } from 'src/app/models/field';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { Form } from 'src/app/models/form';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class FormComponent implements OnInit, OnChanges{
  @Input() fields!: Field[];

  form = new FormGroup({});
  messsage: string = '';
  showMessage: boolean = false;
  info: string = '';
  error: string = '';

  constructor(
    private cookieService: CookieService,
    private apiService: ApiService,
  ) {  }

  ngOnChanges(): void {
    this.fields.forEach(field => {
      this.form.addControl(field.name, new FormControl(null, []));
      if (field.required) {
        (this.form.controls as FormControl[])[field.name as any].setValidators([Validators.required]);
      }

      if (field.type === 'email') {
        (this.form.controls as FormControl[])[field.name as any].setValidators([Validators.email]);
      }

      if (field.type === 'textarea') {
        (this.form.controls as FormControl[])[field.name as any].setValidators([Validators.maxLength(500)]);
      }

      if (field.type === 'phone') {
        (this.form.controls as FormControl[])[field.name as any].setValidators([
          Validators.pattern('^[0-9]*$'),
          Validators.minLength(10),
          Validators.maxLength(10)
        ]);
      }
    });
  }

  ngOnInit(): void {
    console.log(this.form);
    console.log(this.form.value);
  }

  onSubmit() {
    const user_uuid = this.cookieService.get('user_uuid');
    console.log(this.form.value);
    
    const form: Form = {
      userUUID: user_uuid,
      data: this.form.value,
    }

    this.apiService.postForm(form).subscribe((response: any) => {
      this.form.reset();
      this.apiService.fetchLoans(user_uuid);
    }, (error) => {
      for (let key of Object.keys(error.error.message)) {
        this.error += `${key}: ${error.error.message[key]}`;
      }
      this.showMessage = true;
    });

  };

  getErrorMessage(control: FormControl): boolean {
    // Passa em cada erro e faz um switch para retornar a mensagem de erro -> erros padrões do angular https://angular.io/api/forms/Validators
    // Se for um erro customizado, retorna a mensagem de erro customizada que é o valor da chave do erro.
    if (control.invalid && control.touched) {
      if (control.errors) {
        console.log(control.errors);
        const errors = Object.keys(control.errors);
        if (errors.length > 0) {
          this.messsage = '';
          errors.forEach((error) => {
            switch (error) {
              case 'required':
                this.messsage = 'Campo obrigatório.';
                return true;
              case 'email':
                this.messsage = 'E-mail inválido.';
                return true;
              case 'minlength':
                this.messsage = `Mínimo de ${
                  control.errors!['minlength'].requiredLength
                } caracteres.`;
                return true;
              case 'maxlength':
                this.messsage = `Máximo de ${
                  control.errors!['maxlength'].requiredLength
                } caracteres.`;
                return true;
              default:
                this.messsage = control.errors![error];
                return true;
            }
          });
        } else {
          this.messsage = '';
          return false;
        }
      } else {
        this.messsage = '';
        return false;
      }
    } else {
      this.messsage = '';
      return false;
    }
    return false;
  };

  ngOnDestroy(): void {
    this.form.reset();
  }

}
