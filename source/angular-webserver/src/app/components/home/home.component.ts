import { Component } from '@angular/core';
import { MsalService } from '@azure/msal-angular';
import { AuthService } from 'src/app/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: [
    './home.component.scss',
    '../../../assets/vendor/aos/aos.css',
    '../../../assets/vendor/bootstrap/css/bootstrap.min.css',
    '../../../assets/vendor/bootstrap-icons/bootstrap-icons.css',
    '../../../assets/vendor/glightbox/css/glightbox.min.css',
    '../../../assets/vendor/remixicon/remixicon.css',
    '../../../assets/vendor/swiper/swiper-bundle.min.css',
    '../../../assets/css/style.css'

  ]
})
export class HomeComponent {

  title = 'angular-webserver';
  username = 'Gast';

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
    this.username = this.msalService.instance.getActiveAccount()?.name || "Gast";
  }
}
