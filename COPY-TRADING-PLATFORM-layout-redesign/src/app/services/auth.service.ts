import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly AUTH_KEY = 'copy_trading_auth_token';

  // Reactive state management using Angular signals
  private isLoggedInSignal = signal<boolean>(this.checkAuth());
  
  readonly isLoggedIn = this.isLoggedInSignal.asReadonly();

  private checkAuth(): boolean {
    if (typeof window !== 'undefined' && window.localStorage) {
      return localStorage.getItem(this.AUTH_KEY) === 'true';
    }
    return false;
  }

  isAuthenticated(): boolean {
    return this.isLoggedInSignal();
  }

  login(username: string, password: string): boolean {
    // Hardcoded static credentials
    if (username === 'admin' && password === 'admin123') {
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.setItem(this.AUTH_KEY, 'true');
      }
      this.isLoggedInSignal.set(true);
      return true;
    }
    return false;
  }

  logout(): void {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.removeItem(this.AUTH_KEY);
    }
    this.isLoggedInSignal.set(false);
  }
}
