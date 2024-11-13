import { Routes } from '@angular/router';
import { SignupLoginComponent } from './pages/signup-login/signup-login.component';
import { AiChatComponent } from './pages/ai-chat/ai-chat.component';

export const routes: Routes = [
  { path: '', redirectTo: 'signup', pathMatch: 'full' },
  { path: 'signup', component: SignupLoginComponent },
  { path: 'aiChat', component: AiChatComponent },
  { path: '**', redirectTo: 'signup' } // Alle ungültigen Routen zu 'signup' umleiten
];

