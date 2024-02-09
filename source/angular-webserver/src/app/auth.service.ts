import { Injectable } from '@angular/core';
import { PublicClientApplication, AuthError, AuthenticationResult } from '@azure/msal-browser';
import { msalConfig } from './auth-config';
import { MsalService } from '@azure/msal-angular';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private app: PublicClientApplication;
  private isMsalInitialized: boolean = false;

  constructor(private msalService: MsalService) {
    this.app = new PublicClientApplication(msalConfig);
    this.initializeMsal();
  }

  private async initializeMsal(): Promise<void> {
    try {
      await this.app.initialize();
      await this.app.handleRedirectPromise();
      this.isMsalInitialized = true; 
    } catch (error) {
      console.error('MSAL initialization error:', error);
    }
  }

  async login(): Promise<void> {
    if (!this.isMsalInitialized) {
      await this.initializeMsal();
    }

    try {
      const loginResponse = await this.app.loginPopup({
        scopes: ['openid', 'profile', 'User.Read'],
      }).then( (response: AuthenticationResult) => {
        this.msalService.instance.setActiveAccount(response.account);
      });
      console.log('Login successful', loginResponse);
    } catch (error) {
      if (error instanceof AuthError) {
        console.error('Authentication error:', error.errorMessage);
      } else {
        console.error('Unexpected error during login:', error);
      }
    }
  }

  logout(): void {
    this.app.logout();
  }
}