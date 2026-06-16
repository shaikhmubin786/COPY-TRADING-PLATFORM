import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-logs',
  imports: [NgFor],
  templateUrl: './logs.html',
  styleUrl: './logs.css'
})
export class Logs {
  logs = [
    {
      time: '10:35 AM',
      title: 'BUY NIFTY 24500 CE copied successfully',
      type: 'Success',
      typeClass: 'success',
      dotClass: 'dot-success',
      message: 'Master order was copied to AliceBlue child account with 1x multiplier.',
      broker: 'AliceBlue',
      account: 'ACC002',
      symbol: 'NIFTY 24500 CE',
      category: 'Copy Log'
    },
    {
      time: '10:38 AM',
      title: 'Auto retry triggered',
      type: 'Retry',
      typeClass: 'retry',
      dotClass: 'dot-retry',
      message: 'Initial order failed due to timeout. System started retry attempt 1 of 3.',
      broker: 'Zenam',
      account: 'ACC003',
      symbol: 'BANKNIFTY 52000 PE',
      category: 'Retry Log'
    },
    {
      time: '10:41 AM',
      title: 'Broker API response received',
      type: 'API',
      typeClass: 'api',
      dotClass: 'dot-api',
      message: 'Zerodha WebSocket sent order update response to copy engine.',
      broker: 'Zerodha',
      account: 'ACC001',
      symbol: 'RELIANCE',
      category: 'API Response'
    },
    {
      time: '10:45 AM',
      title: 'Access token expired',
      type: 'Error',
      typeClass: 'error',
      dotClass: 'dot-error',
      message: 'Child order rejected because broker access token expired. Reconnect required.',
      broker: 'Zenam',
      account: 'ACC003',
      symbol: 'TCS',
      category: 'Error Log'
    }
  ];
}