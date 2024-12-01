import { Routes } from '@angular/router';
import { AiChatComponent } from './pages/ai-chat/ai-chat.component';

export const routes: Routes = [
  { path: '', redirectTo: 'aiChat', pathMatch: 'full' },
  { path: 'aiChat', component: AiChatComponent },
  { path: '**', redirectTo: 'aiChat' } // Alle ungültigen Routen zu 'aiChat' umleiten
];

