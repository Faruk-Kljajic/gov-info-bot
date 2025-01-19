import { Component, Input, AfterViewChecked, ElementRef, ViewChild, Renderer2} from '@angular/core';
import {isPlatformBrowser, NgClass, NgForOf} from '@angular/common';
import { Inject, PLATFORM_ID } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';


@Component({
  selector: 'app-messages',
  standalone: true,
  templateUrl: './messages.component.html',
  imports: [
    NgClass,
    NgForOf
  ],
  styleUrl: './messages.component.css'
})
export class MessagesComponent implements AfterViewChecked {
  @Input() messages: { sender: string; text: string }[] = [];

  // Nachrichten-Container referenzieren
  @ViewChild('messagesContainer', { static: false }) messagesContainer!: ElementRef;

  constructor(
    private sanitizer: DomSanitizer,
    @Inject(PLATFORM_ID) private platformId: Object,
    private renderer: Renderer2,
  ) {}

  ngAfterViewChecked() {
    if (isPlatformBrowser(this.platformId)) {
      // Scrollen mithilfe von Renderer2
      this.scrollToBottom();
    }
  }

  private scrollToBottom() {
    if (this.messagesContainer) {
      this.renderer.setProperty(
        this.messagesContainer.nativeElement,
        'scrollTop',
        this.messagesContainer.nativeElement.scrollHeight
      );
    }
  }

   // Funktion, um den Text als HTML zu rendern
  renderText(text: string) {
    return this.sanitizer.bypassSecurityTrustHtml(text);
  }

}
