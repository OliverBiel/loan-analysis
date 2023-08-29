import { Component } from '@angular/core';
import { Field } from './models/field';
import { ApiService } from './services/api.service';
import { CookieService } from 'ngx-cookie-service';
import { uuid } from './models/uuid';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'loan-analysis';
  form: Field[] = [];

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
  ) { }

  ngOnInit(): void {
    this.apiService.getFields().subscribe((fields: Field[] | {}) => {
      this.form = fields as Field[];
    });

    if (this.cookieService.get('user_uuid') === '') {
      this.apiService.getUUID().subscribe((uuid: uuid) => {
        this.cookieService.set('user_uuid', uuid.user_uuid, { expires: 365, path: '/', sameSite: 'Strict'});
      })
    }

  }
}
