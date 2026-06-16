import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-positions',
  imports: [NgFor],
  templateUrl: './positions.html',
  styleUrl: './positions.css'
})
export class Positions {
  positions = [
    {
      broker: 'Zerodha',
      account: 'ACC001 Master Account',
      symbol: 'NIFTY 24500 CE',
      side: 'BUY',
      sideClass: 'buy',
      qty: 50,
      avg: '₹125.40',
      ltp: '₹132.80',
      mtm: '+₹370',
      pnl: '+₹370',
      pnlClass: 'profit',
      status: 'Live position synced 2 seconds ago'
    },
    {
      broker: 'AliceBlue',
      account: 'ACC002 Child Account',
      symbol: 'NIFTY 24500 CE',
      side: 'BUY',
      sideClass: 'buy',
      qty: 100,
      avg: '₹125.80',
      ltp: '₹132.90',
      mtm: '+₹710',
      pnl: '+₹710',
      pnlClass: 'profit',
      status: 'Copied position running with 2x multiplier'
    },
    {
      broker: 'Zenam',
      account: 'ACC003 Child Account',
      symbol: 'BANKNIFTY 52000 PE',
      side: 'SELL',
      sideClass: 'sell',
      qty: 30,
      avg: '₹210.10',
      ltp: '₹214.30',
      mtm: '-₹126',
      pnl: '-₹126',
      pnlClass: 'loss',
      status: 'Position active, slippage within limit'
    }
  ];
}