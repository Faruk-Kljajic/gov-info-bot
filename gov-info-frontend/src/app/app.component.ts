import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import {AiChatComponent} from "./pages/ai-chat/ai-chat.component";

@Component( {
  selector: 'app-root',
  standalone: true,
    imports: [CommonModule, RouterOutlet, AiChatComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
} )
export class AppComponent {
  title = 'ai-chatbot-frontend';
}
