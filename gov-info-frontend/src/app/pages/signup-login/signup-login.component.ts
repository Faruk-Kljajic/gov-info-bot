import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { Router } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component( {
  selector: 'app-signup-login',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatDialogModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './signup-login.component.html',
  styleUrl: './signup-login.component.scss'
} )
export class SignupLoginComponent implements OnInit{
  private router = inject(Router);
  userForm: FormGroup;

  constructor(private _fb: FormBuilder){
    this.userForm = this._fb.group( {
      username: ''
    } );
  }

  ngOnInit(): void{
  }

navigateToAIChat() {
  console.log('Button wurde geklickt - Navigation wird versucht');
  sessionStorage.setItem('username', this.userForm.value.username);
  this.router.navigate(['aiChat']).then(success => {
    if (success) {
      console.log('Navigation erfolgreich');
    } else {
      console.error('Navigation fehlgeschlagen');
    }
  });
}



}
