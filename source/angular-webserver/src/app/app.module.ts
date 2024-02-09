//New imports
import { MSAL_INSTANCE, MsalModule, MsalService } from '@azure/msal-angular';
import { IPublicClientApplication, PublicClientApplication } from '@azure/msal-browser';
//New imports

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';


export function MSALInstanceFactory() : IPublicClientApplication {
  return new PublicClientApplication({
    auth: {
      clientId: '30a4b95d-3e03-4b2a-ae30-7acdb2a3af21',
      authority: 'https://login.microsoftonline.com/91fc072c-edef-4f97-bdc5-cfb67718ae3a',
      redirectUri: 'http://localhost:4200'
    },
    cache: {
      cacheLocation: 'localStorage',
      storeAuthStateInCookie: true
    }
    }
  );
}

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    //New imports
    MsalModule
    //New imports
  ],
  providers: [
    {
      provide: MSAL_INSTANCE,
      useFactory: MSALInstanceFactory
    },
    //Authentication service
    MsalService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
