import { Component, OnInit } from '@angular/core';
import { MsalService } from '@azure/msal-angular';
import { AuthenticationResult } from '@azure/msal-browser';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'angular-webserver';
  username = 'guest';

  //constructor
  constructor(private authService: AuthService, private msalService : MsalService) {}

  ngOnInit(): void {
    this.updateUsername();
  }

  //Method to check if the user is logged in
  isLoggedIn() : boolean {
    return this.msalService.instance.getActiveAccount() !== null ? true : false;
  }

  async login(): Promise<void> {
    if (!this.isLoggedIn()) {
      await this.authService.login();
    }
    this.updateUsername();
  }

  logout(): void {
    if (this.isLoggedIn()) {
      this.authService.logout();
    }
    this.updateUsername();
  }

  updateUsername() {
    this.username = this.msalService.instance.getActiveAccount()?.name || "guest";
  }
}
