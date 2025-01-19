import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChatService } from './services/chat.service';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  imports: [FormsModule, CommonModule] // FormsModule ist für ngModel notwendig
})
export class AppComponent {
  title = 'ai-chatbot-frontend';
  message: string = ''; // Nachricht des Nutzers
  messages: Array<{ text: string; sender: string }> = []; // Nachrichtenliste
  isRagEnabled: boolean = false; // Zustand von RAG
  chatHistory: string[] = [];

  constructor(private chatService: ChatService) {}


  handleUserMessage(): void {
    if (this.message.trim()) {
      // Nachricht des Nutzers zur Anzeige hinzufügen
      this.messages.push({ sender: 'user', text: this.message });

      // Nachricht an den Service weitergeben
      this.chatService.sendMessage(this.message, this.isRagEnabled).subscribe({
        next: (response) => {
          // Antwort vom Backend zur Anzeige hinzufügen
          this.messages.push({ sender: 'bot', text: response.response });
        },
        error: (error) => {
          // Fehlerbehandlung
          console.error('Fehler bei der Backend-Anfrage:', error);
          this.messages.push({ sender: 'bot', text: 'Fehler beim Abrufen der Antwort vom Backend.' });
        },
      });

      // Eingabefeld leeren
      this.message = '';
    }
  }

  toggleRAG(): void {
    this.isRagEnabled = !this.isRagEnabled;
    console.log(`RAG ist jetzt ${this.isRagEnabled ? 'aktiviert' : 'deaktiviert'}`);
  }

  archiveConversation(): void {
    console.log('Konversation archiviert.');
    // Archivierungslogik hier ergänzen
  }
}
