
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { Router } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { environment } from '../../../environments/environment.development';
import { Injectable } from '@angular/core';
import { Client, Message, Stomp } from '@stomp/stompjs';
import { Observable, Subject } from 'rxjs';
import { WebsocketService } from '../../service/websocket.service';
import SockJS from 'sockjs-client';

@Component({
  selector: 'app-ai-chat',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatDialogModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './ai-chat.component.html',
  styleUrl: './ai-chat.component.scss'
})
export class AiChatComponent implements OnInit {
  constructor(
    private _stompService: WebsocketService
  ) {}
  ngOnInit(): void {
    this._stompService.subscribe('topic/public', (): any => {
      console.log('message received');
    })
  }
}
