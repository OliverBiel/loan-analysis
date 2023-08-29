import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoanOrderComponent } from './loan-order.component';

describe('LoanOrderComponent', () => {
  let component: LoanOrderComponent;
  let fixture: ComponentFixture<LoanOrderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoanOrderComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoanOrderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
