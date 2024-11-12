import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000';
  constructor(private http: HttpClient) { }

  // GET-Anfrage für eine Begrüßung
  getGreeting(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/`);
  }

  // POST-Anfrage für eine Berechnung
  calculate(value: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/chat/`, { value });
  }
}
