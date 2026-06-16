import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-notifications',
  imports: [NgFor],
  templateUrl: './notifications.html',
  styleUrl: './notifications.css'
})
export class Notifications {
  summaryCards = [
    {
      icon: '✅',
      iconClass: 'summary-icon icon-green',
      title: 'Trade Alerts',
      badgeClass: 'summary-badge badge-green',
      value: '42',
      description: 'Successful trade notifications'
    },
    {
      icon: '🔁',
      iconClass: 'summary-icon icon-yellow',
      title: 'Retry Alerts',
      badgeClass: 'summary-badge badge-yellow',
      value: '09',
      description: 'Auto retry updates'
    },
    {
      icon: '⚠️',
      iconClass: 'summary-icon icon-red',
      title: 'Broker Warnings',
      badgeClass: 'summary-badge badge-red',
      value: '04',
      description: 'Token and session issues'
    },
    {
      icon: '🔔',
      iconClass: 'summary-icon icon-blue',
      title: 'System Alerts',
      badgeClass: 'summary-badge badge-blue',
      value: '16',
      description: 'Platform updates'
    }
  ];

  alertRules = [
    {
      priority: 'High Priority',
      title: 'Broker token expired',
      description: 'Immediately notify admin when access token becomes invalid.'
    },
    {
      priority: 'Medium Priority',
      title: 'Retry executed',
      description: 'Notify when failed order is retried by the system.'
    },
    {
      priority: 'Info',
      title: 'Market open validation',
      description: 'Notify when copy engine becomes ready for market hours.'
    }
  ];

  notifications = [
    {
      icon: '✅',
      iconClass: 'icon-success',
      title: 'BUY Order Copied',
      message: 'NIFTY 24500 CE was copied successfully from master to AliceBlue child account.',
      time: '2 min ago',
      type: 'Trade',
      typeClass: 'success',
      broker: 'AliceBlue',
      account: 'ACC002',
      category: 'Order Copy'
    },
    {
      icon: '⚠️',
      iconClass: 'icon-warning',
      title: 'Retry Executed',
      message: 'Order failed due to timeout. Auto retry executed and order was processed successfully.',
      time: '15 min ago',
      type: 'Retry',
      typeClass: 'warning',
      broker: 'Zenam',
      account: 'ACC003',
      category: 'Auto Retry'
    },
    {
      icon: '❌',
      iconClass: 'icon-danger',
      title: 'Access Token Expired',
      message: 'Zenam broker session expired. Reconnect API before starting copy trading.',
      time: '28 min ago',
      type: 'Warning',
      typeClass: 'danger',
      broker: 'Zenam',
      account: 'ACC003',
      category: 'Broker Session'
    },
    {
      icon: 'ℹ️',
      iconClass: 'icon-info',
      title: 'Market Open',
      message: 'Market time validation passed. Copy trading engine is ready for live execution.',
      time: '09:15 AM',
      type: 'System',
      typeClass: 'info',
      broker: 'System',
      account: 'All Accounts',
      category: 'Market Timing'
    }
  ];
}