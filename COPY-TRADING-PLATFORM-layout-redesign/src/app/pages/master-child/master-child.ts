import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-master-child',
  imports: [NgFor],
  templateUrl: './master-child.html',
  styleUrl: './master-child.css'
})
export class MasterChild {
  children = [
    {
      short: 'A',
      account: 'AliceBlue Child 01',
      clientId: 'ACC002',
      broker: 'AliceBlue',
      multiplier: '1x',
      copyEnabled: true,
      status: 'Active',
      statusClass: 'active',
      sync: '2 sec ago'
    },
    {
      short: 'Z',
      account: 'Zenam Child 02',
      clientId: 'ACC003',
      broker: 'Zenam',
      multiplier: '2x',
      copyEnabled: true,
      status: 'Active',
      statusClass: 'active',
      sync: '5 sec ago'
    },
    {
      short: 'Z',
      account: 'Zerodha Child 03',
      clientId: 'ACC004',
      broker: 'Zerodha',
      multiplier: '0.5x',
      copyEnabled: false,
      status: 'Paused',
      statusClass: 'paused',
      sync: '1 min ago'
    }
  ];
}