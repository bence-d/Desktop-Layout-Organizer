import { Component } from '@angular/core';
import { MsalService } from '@azure/msal-angular';
import { AuthenticationResult } from '@azure/msal-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'angular-webserver';

  //constructor
  constructor(private msalService : MsalService) {

  }

  //Method to check if the user is logged in
  isLoggedIn() : boolean{
    return this.msalService.instance.getActiveAccount() != null
  }

  //New method to login
  login() {
    this.msalService.loginPopup().subscribe( (response: AuthenticationResult) => {
      this.msalService.instance.setActiveAccount(response.account)
    });
  }

  //New method to logout
  logout() {
    this.msalService.logout();
  }
}
