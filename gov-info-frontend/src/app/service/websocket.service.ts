import { Injectable } from '@angular/core';
import { Stomp } from '@stomp/stompjs';
// import { Client, Message, Stomp } from '@stomp/stompjs';
import { Observable, Subject } from 'rxjs';
import SockJS from 'sockjs-client';
// import * as SockJS from 'sockjs-client';
// import * as Stomp from 'stompjs';

@Injectable( {
  providedIn: 'root'
} )
export class WebsocketService {
  socket = new SockJS('http://localhost:8080/ws');
  stompClient = Stomp.over(this.socket);

  subscribe(topic: string, callback: any): void{
    const connected: boolean = this.stompClient.connected;
    if(connected){
      this.subscribeToTopic(topic, callback);
      return;
    }

    this.stompClient.connect({}, (): any => {
      this.subscribeToTopic(topic, callback);
    } );
  }

  private subscribeToTopic(topic: string, callback: any): void {
    this.stompClient.subscribe(topic, (): any => {
      callback();
    } );
  }

  addUser(message: string): void{
  }

  sendMessage(message: string): void {
    this.stompClient.send('/app/chat.sendMessage', {}, message);
  }
}
