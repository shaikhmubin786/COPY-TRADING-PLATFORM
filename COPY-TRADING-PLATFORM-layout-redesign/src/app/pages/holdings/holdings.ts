import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-holdings',
  imports: [NgFor],
  templateUrl: './holdings.html',
  styleUrl: './holdings.css'
})
export class Holdings {
  holdings = [
    {
      broker: 'Zerodha',
      account: 'ACC001 Master Account',
      symbol: 'RELIANCE',
      qty: 25,
      avg: '₹2,710',
      ltp: '₹2,842',
      invested: '₹67,750',
      value: '₹71,050',
      pnl: '+₹3,300',
      pnlClass: 'profit',
      status: 'Holding synced with master account'
    },
    {
      broker: 'AliceBlue',
      account: 'ACC002 Child Account',
      symbol: 'TCS',
      qty: 15,
      avg: '₹3,820',
      ltp: '₹3,920',
      invested: '₹57,300',
      value: '₹58,800',
      pnl: '+₹1,500',
      pnlClass: 'profit',
      status: 'Child holding mapped successfully'
    },
    {
      broker: 'Zenam',
      account: 'ACC003 Child Account',
      symbol: 'INFY',
      qty: 40,
      avg: '₹1,520',
      ltp: '₹1,498',
      invested: '₹60,800',
      value: '₹59,920',
      pnl: '-₹880',
      pnlClass: 'loss',
      status: 'Holding active, current value updated'
    }
  ];
}