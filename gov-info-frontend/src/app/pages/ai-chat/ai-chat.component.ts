
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import {ChatService} from "../../service/chat.service";
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

  constructor(private apiService: ChatService) {}

  ngOnInit(): void {}

  sendMessage(): void {
    if (this.message.trim()) {
      this.messages.push({ sender: 'user', text: this.message });

      // Anfrage an das Backend senden
      this.apiService.sendMessage(this.message).subscribe(
        (response) => {
          this.messages.push({ sender: 'bot', text: response.response });
        },
        (error) => {
          console.error('Error:', error);
          this.messages.push({ sender: 'bot', text: 'Server error, please try again later.' });
        }
      );

      this.message = ''; // Eingabefeld zurücksetzen
    }
  }

}
