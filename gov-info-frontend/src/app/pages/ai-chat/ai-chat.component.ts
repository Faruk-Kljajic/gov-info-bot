
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { Router } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import {ApiService} from "../../service/api.service";
import {CommonModule, NgClass} from "@angular/common";

@Component({
  selector: 'app-ai-chat',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatDialogModule,
    MatInputModule,
    MatButtonModule,
    NgClass,
    CommonModule
  ],
  templateUrl: './ai-chat.component.html',
  styleUrl: './ai-chat.component.scss'
})
export class AiChatComponent implements OnInit {
  message: string = '';
  messages: Array<{ text: string, sender: string }> = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {}

  //Sendet Nachricht an Backend
sendMessage(): void {
  if (this.message.trim() === '') return;

  // Zeige die Benutzernachricht
  this.messages.push({ text: this.message, sender: 'user' });

  // Sende Nachricht an das Backend und hole Antwort
  this.apiService.sendMessage(this.message).subscribe(response => {
    // Antwort vom Chatbot anzeigen
    this.messages.push({ text: response.response, sender: 'bot' });
  }, error => {
    console.error('Fehler beim Senden der Nachricht:', error);
  });

  // Eingabefeld leeren
  this.message = '';
}

}
