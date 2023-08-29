import { Component } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Subscription, interval } from 'rxjs';
import { Loan } from 'src/app/models/loan';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-loan-order',
  templateUrl: './loan-order.component.html',
  styleUrls: ['./loan-order.component.scss']
})
export class LoanOrderComponent {

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
  ) { }

  timeInterval!: Subscription;
  loans: Loan[] = [];

  ngOnInit(): void {
    const user_uuid = this.cookieService.get('user_uuid');
    this.apiService.fetchLoans(user_uuid);
    
    this.apiService.loans.subscribe((loans: Loan[]|{}) => {
      this.loans = loans as Loan[];
    });

    this.timeInterval = interval(10000).subscribe(() => {
      this.apiService.fetchLoans(user_uuid);
    });

  }

}
