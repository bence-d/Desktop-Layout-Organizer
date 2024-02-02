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
  username = 'not logged in';

  //constructor
  constructor(private msalService : MsalService) {}

  //Method to check if the user is logged in
  isLoggedIn() : boolean{
    if (this.msalService.instance.getActiveAccount() != null) {
      this.username = this.msalService.instance.getActiveAccount()?.name || "not logged in";
    }
    return this.msalService.instance.getActiveAccount() != null
  }
}
