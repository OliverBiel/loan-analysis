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
  uuid: string = '';

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
  ) { }

  ngOnInit(): void {
    if (this.cookieService.get('user_uuid') === '') {
      this.apiService.fetchUUID();
    } else {
      this.apiService.uuid.next(this.cookieService.get('user_uuid'));
    }

    this.apiService.uuid.subscribe((uuid: string) => {
      this.uuid = uuid;
      this.cookieService.set('user_uuid', uuid);
    });

    this.apiService.fetchLoans(this.uuid);

    this.apiService.getFields().subscribe((fields: Field[] | {}) => {
      this.form = fields as Field[];
    });
  }
}
