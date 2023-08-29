import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Field } from '../models/field';
import { BehaviorSubject, Observable } from 'rxjs';
import { uuid } from '../models/uuid';
import { Form } from '../models/form';
import { Loan } from '../models/loan';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
  ) { }

  loans: BehaviorSubject<Loan[] | {}> = new BehaviorSubject<Loan[] | {}>([] as Loan[]);
  uuid: BehaviorSubject<string> = new BehaviorSubject<string>('');

  getFields(): Observable<Field[] | {}> {
    return this.http.get<Field[] | {}>(environment.apiUrl + '/fields/');
  }

  getUUID(): Observable<uuid> {
    return this.http.get<uuid>(environment.apiUrl + '/uuid/');
  }

  fetchUUID() {
    this.getUUID().subscribe((response: any) => {
      this.uuid.next(response.user_uuid);
    });
  }

  postForm(form: Form): Observable<any> {
    return this.http.post<any>(environment.apiUrl + '/loan/', form);
  }

  getLoans(uuid: string): Observable<Loan[] | {}> {
    return this.http.get<Loan[] | {}>(environment.apiUrl + '/loans/' + uuid);
  }

  fetchLoans(user_uuid: string) {
    this.getLoans(user_uuid).subscribe((response: any) => {
      this.loans.next(response as Loan[]);
    });
  }

}
