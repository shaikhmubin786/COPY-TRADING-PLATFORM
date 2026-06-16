import {
  Component,
  OnInit,
  ChangeDetectorRef
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {

  stats: any[] = [];
  accountSummary: any[] = [];
  symbolSummary: any[] = [];

constructor(
  private http: HttpClient,
  private cd: ChangeDetectorRef
) {}

 ngOnInit(): void {
  console.clear();

  console.log("🚀 START");

  this.loadDashboard();
  this.loadAccounts();
  this.loadTrades();

  

}

  // Dashboard Cards
  loadDashboard() {

  this.http.get('http://127.0.0.1:8000/api/dashboard',
  {
    observe: 'response',
    responseType: 'text'
  })
  .subscribe({
    next: (res) => {

      console.log("RAW RESPONSE", res);

      const data = JSON.parse(res.body || '{}');

      this.stats = [
  {
    label: 'Total Accounts',
    value: data.total_accounts,
    info: 'All broker accounts'
  },
  {
    label: 'Total Mappings',
    value: data.total_mappings,
    info: 'Master Child Mappings'
  },
  {
    label: 'Active Mappings',
    value: data.active_mappings,
    info: 'Running Copy Trading'
  },
  {
    label: 'Child Trades',
    value: data.total_child_trades,
    info: 'Copied Trades'
  }
];
      this.cd.detectChanges();

      console.log("AFTER SET", this.stats.length);
    },

    error: (err) => {
      console.log("ERROR API", err);
    }
  });
}

  // Account Table
  loadAccounts() {

    this.http.get<any>('http://127.0.0.1:8000/api/accounts')
      .subscribe({

        next: (res) => {

          console.log("Accounts API:", res);

          const accounts = res?.accounts || [];

          this.accountSummary = accounts.map((acc: any) => ({
            pseudo: acc.client_id || "-",
            trading: acc.broker || "-",

            m2m: "₹0",
            pnl: "₹0",
            pnlClass: "profit",
            atPnl: "₹0",

            total: 0,
            open: 0,
            closed: 0,

            marginTotal: "₹0",
            utilized: "₹0",
            available: "₹0",

            orderTotal: 0,
            orderOpen: 0,
            pending: 0,
            complete: 0
          }));
          this.cd.detectChanges();

          console.log(
            "Account Summary Final:",
            this.accountSummary
          );

        },

        error: (error) => {
          console.error(
            "Accounts API Error:",
            error
          );
        }

      });

  }


  // Trades Table
  loadTrades() {

    this.http.get<any>('http://127.0.0.1:8000/api/trades')
      .subscribe({

        next: (res) => {

          console.log("Trades API:", res);

          const trades = res?.trades || [];

          this.symbolSummary = trades.map((trade: any) => ({

            symbol: trade.symbol || "-",

            buyQty:
              trade.side === "BUY"
                ? trade.quantity : 0,

            sellQty:
              trade.side === "SELL"
                ? trade.quantity : 0,

            netQty: trade.quantity || 0,

            m2m: "₹0",
            pnl: "₹0",
            pnlClass: "profit",

            buyAvg: "0",
            sellAvg: "0",

            holdingQty: 0,
            value: "₹0",

            totalQty: trade.quantity || 0,

            status: trade.status || "Unknown",

            statusClass:
              trade.status === "EXECUTED"
                ? "live"
                : "warning",

            broker: "Copy Trade"

          }));
          this.cd.detectChanges();

          console.log(
            "Symbol Summary Final:",
            this.symbolSummary
          );

        },

        error: (error) => {

          console.error(
            "Trades API Error:",
            error
          );

        }

      });

  }

}