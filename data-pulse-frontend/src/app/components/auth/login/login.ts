import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router,RouterModule } from '@angular/router';
import { AuthService } from '../../../core/auth/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,RouterModule],
  templateUrl: './login.html' // <-- Verifica que tu archivo HTML se llame exactamente login.html
})
export class Login {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  // Usamos nonNullable para que TypeScript no se queje de que los valores pueden ser null
  loginForm = this.fb.nonNullable.group({
    username: ['', [Validators.required]],
    password: ['', [Validators.required]]
  });

  errorMessage: string = '';

  onSubmit() {
    if (this.loginForm.valid) {
      // getRawValue() obtiene los datos limpios del formulario
      const credentials = this.loginForm.getRawValue();

      this.authService.login(credentials).subscribe({
        next: (res) => {
          console.log('Login exitoso');
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          this.errorMessage = 'Usuario o contraseña incorrectos';
          console.error(err);
        }
      });
    }
  }
}