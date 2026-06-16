import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { Accounts } from './pages/accounts/accounts';
import { MasterChild } from './pages/master-child/master-child';
import { Orders } from './pages/orders/orders';
import { Positions } from './pages/positions/positions';
import { Holdings } from './pages/holdings/holdings';
import { Logs } from './pages/logs/logs';
import { Settings } from './pages/settings/settings';
import { RiskManagement } from './pages/risk-management/risk-management';
import { Notifications } from './pages/notifications/notifications';
import { BrokerSettings } from './pages/broker-settings/broker-settings';
import { Reports } from './pages/reports/reports';
import { OwnerLogin } from './pages/owner-login/owner-login';
import { LayoutComponent } from './layout/layout';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'owner-login', component: OwnerLogin },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', component: Dashboard },
      { path: 'accounts', component: Accounts },
      { path: 'master-child', component: MasterChild },
      { path: 'orders', component: Orders },
      { path: 'positions', component: Positions },
      { path: 'holdings', component: Holdings },
      { path: 'logs', component: Logs },
      { path: 'settings', component: Settings },
      { path: 'risk-management', component: RiskManagement },
      { path: 'notifications', component: Notifications },
      { path: 'broker-settings', component: BrokerSettings },
      { path: 'reports', component: Reports },
    ]
  }
];