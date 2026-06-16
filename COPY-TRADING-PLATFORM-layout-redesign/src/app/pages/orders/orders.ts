import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-orders',
  imports: [NgFor],
  templateUrl: './orders.html',
  styleUrl: './orders.css'
})
export class Orders {
  orders = [
    {
      time: '10:35 AM',
      master: 'Zerodha ACC001',
      child: 'AliceBlue ACC002',
      symbol: 'NIFTY 24500 CE',
      action: 'BUY',
      actionClass: 'buy',
      qty: 50,
      price: '₹125.40',
      multiplier: '1x',
      status: 'Completed',
      statusClass: 'completed',
      message: 'Copied successfully from master to child account.'
    },
    {
      time: '10:36 AM',
      master: 'Zerodha ACC001',
      child: 'Zenam ACC003',
      symbol: 'NIFTY 24500 CE',
      action: 'BUY',
      actionClass: 'buy',
      qty: 100,
      price: '₹125.80',
      multiplier: '2x',
      status: 'Completed',
      statusClass: 'completed',
      message: 'Executed instantly with quantity multiplier.'
    },
    {
      time: '10:38 AM',
      master: 'Zerodha ACC001',
      child: 'Zerodha ACC004',
      symbol: 'BANKNIFTY 52000 PE',
      action: 'SELL',
      actionClass: 'sell',
      qty: 30,
      price: '₹210.10',
      multiplier: '0.5x',
      status: 'Pending',
      statusClass: 'pending',
      message: 'Waiting for broker API response.'
    },
    {
      time: '10:41 AM',
      master: 'Zerodha ACC001',
      child: 'AliceBlue ACC002',
      symbol: 'RELIANCE',
      action: 'MODIFY',
      actionClass: 'modify',
      qty: 10,
      price: '₹2,842',
      multiplier: '1x',
      status: 'Completed',
      statusClass: 'completed',
      message: 'Child order modified successfully.'
    },
    {
      time: '10:45 AM',
      master: 'Zerodha ACC001',
      child: 'Zenam ACC003',
      symbol: 'TCS',
      action: 'CANCEL',
      actionClass: 'cancel',
      qty: 5,
      price: '₹3,920',
      multiplier: '1x',
      status: 'Rejected',
      statusClass: 'rejected',
      message: 'Order rejected because access token expired.'
    }
  ];
}