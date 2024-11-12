import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
declare var SockJS: any;
declare var Stomp: any;

@Injectable( {
  providedIn: 'root'
} )
export class MessageService{
  constructor() { }
}
