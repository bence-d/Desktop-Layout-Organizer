// src/app/sso/sso.component.ts

import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-sso',
  templateUrl: './sso.component.html',
  styleUrls: ['./sso.component.css'],
})
export class SsoComponent implements OnInit {
  constructor(private authService: AuthService) {}
  ngOnInit(): void {
    this.login();
  }

  login(): void {
    this.authService.login();
  }

  logout(): void {
    this.authService.logout();
  }

  /*
  isLoggedIn() : boolean{
    return this.authService.isLoggedIn();
  }
  */
}
