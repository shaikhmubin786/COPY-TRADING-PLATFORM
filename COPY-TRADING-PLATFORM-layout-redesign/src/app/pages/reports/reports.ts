import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-reports',
  imports: [NgFor],
  templateUrl: './reports.html',
  styleUrl: './reports.css'
})
export class Reports {
  brokerReports = [
    { broker: 'Zerodha', orders: 128, success: '96%', pnl: '+₹18,500', status: 'Excellent' },
    { broker: 'AliceBlue', orders: 94, success: '91%', pnl: '+₹11,200', status: 'Good' },
    { broker: 'Zenam', orders: 52, success: '78%', pnl: '-₹2,400', status: 'Needs Check' }
  ];

  activities = [
    'Highest profit generated from NIFTY 24500 CE.',
    'Zenam failed orders increased due to token expiry.',
    'AliceBlue execution speed improved today.',
    'Retry system recovered 9 failed orders.'
  ];
}