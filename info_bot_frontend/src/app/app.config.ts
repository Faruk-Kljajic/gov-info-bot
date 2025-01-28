import { ApplicationConfig } from '@angular/core';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http';

export const applicationConfig: ApplicationConfig = {
  providers: [
    provideAnimations(),
    provideHttpClient()
  ]
};