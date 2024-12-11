import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
   private apiUrl = 'http://localhost:8000/chat';
  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<any> {
    console.log("Sende Nachricht an Backend:", message); // Debugging
    return this.http.post(`${this.apiUrl}/api/chat`, { message });
  }
}
