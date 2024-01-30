import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SsoComponent } from './sso/sso.component';
import { AppComponent } from './app.component';

const routes: Routes = [
  {path: '', redirectTo: '/sso', pathMatch: 'full'},
  {path: 'sso', component: SsoComponent},
  //{path: 'home', component: AppComponent},
  //{path: '', redirectTo: '/home', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
