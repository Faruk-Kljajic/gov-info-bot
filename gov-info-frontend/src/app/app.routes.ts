import { Routes } from '@angular/router';
import { AiChatComponent } from './pages/ai-chat/ai-chat.component';

export const routes: Routes = [
  { path: '', redirectTo: '/chat', pathMatch: 'full' },
  { path: 'chat', component: AiChatComponent },
  { path: '**', redirectTo: '/chat' } // Alle ungültigen Routen zu 'aiChat' umleiten
];

