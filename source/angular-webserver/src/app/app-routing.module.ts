import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SsoComponent } from './sso/sso.component';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  {path: '', redirectTo: '/home', pathMatch: 'full'},
  {
    path: 'home', component: HomeComponent,
    children: [
      {path: 'sso', component: SsoComponent}
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
