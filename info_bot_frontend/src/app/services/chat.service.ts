import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import {catchError, Observable, throwError} from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private apiUrl = 'http://localhost:8000/api/chat'; // Base-URL des Backends

  constructor(private http: HttpClient) {}

  /**
   * Sendet eine Nachricht an das Backend.
   * @param message Die Benutzeranfrage.
   * @param use_rag Gibt an, ob RAG verwendet werden soll.
   * @returns Observable mit der Antwort des Backends.
   */
  sendMessage(message: string, use_rag: boolean): Observable<any> {
    return this.http
        .post(`${this.apiUrl}/`, { message, use_rag: use_rag })
        .pipe(catchError(this.handleError)); // Fehlerbehandlung, siehe unten
  }

  // Fehlerbehandlung
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Ein unbekannter Fehler ist aufgetreten.';
    if (error.error instanceof ErrorEvent) {
      // Client-seitiger Fehler
      errorMessage = `Fehler: ${error.error.message}`;
    } else {
      // Server-seitiger Fehler
      errorMessage = `Server-Fehler (${error.status}): ${error.message}`;
    }
    return throwError(() => new Error(errorMessage));
  }
}
