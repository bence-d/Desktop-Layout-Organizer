// src/app/sso/sso.component.ts

import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { MsalService } from '@azure/msal-angular';

@Component({
  selector: 'app-sso',
  templateUrl: './sso.component.html',
  styleUrls: ['./sso.component.scss'],
})
export class SsoComponent implements OnInit {
  constructor(private authService: AuthService, private msalService: MsalService) {}
  ngOnInit(): void {
    // if the user gets redirected to this page when they're already logged in, log them out
    if (this.isLoggedIn()) {
      this.logout();
    }
  }

  async login(provider: string): Promise<void> {
    switch (provider) {
      case 'microsoft':
        await this.authService.login();
        break;
      default:
        break;
    }

    window.location.href = '/';
  }

  async logout(): Promise<void> {
    await this.authService.logout();
    window.location.href = '/';
  }

  //Method to check if the user is logged in
  isLoggedIn() : boolean {
    return this.msalService.instance.getActiveAccount() !== null ? true : false;
  }
}
