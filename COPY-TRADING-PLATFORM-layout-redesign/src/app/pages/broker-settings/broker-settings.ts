import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-broker-settings',
  imports: [NgFor],
  templateUrl: './broker-settings.html',
  styleUrl: './broker-settings.css'
})
export class BrokerSettings {
  brokers = [
    {
      short: 'Z',
      name: 'Zerodha',
      api: 'Kite Connect API',
      status: 'Connected',
      statusClass: 'connected',
      session: 'Valid',
      refresh: '2 min ago',
      websocket: 'Active'
    },
    {
      short: 'A',
      name: 'AliceBlue',
      api: 'ANT API',
      status: 'Connected',
      statusClass: 'connected',
      session: 'Valid',
      refresh: '8 min ago',
      websocket: 'API Only'
    },
    {
      short: 'Z',
      name: 'Zenam',
      api: 'API Integration Required',
      status: 'Disconnected',
      statusClass: 'disconnected',
      session: 'Expired',
      refresh: 'Required',
      websocket: 'Inactive'
    }
  ];
}