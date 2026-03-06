import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/auth/services/auth.service';

@Component({
  selector: 'app-register',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  standalone: true,
  templateUrl: './register.html',
  styleUrl: './register.scss',
})
export class Register {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  errorMessage: string = '';
  successMessage: string = '';

  registerForm = this.fb.nonNullable.group({
    nombre_completo: ['', [Validators.required, Validators.minLength(10)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(9)]],
    confirm_password: ['', [Validators.required]]
  }, {
    // Validación personalizada para comparar contraseñas
    validators: (group) => {
      const pass = group.get('password')?.value;
      const confirm = group.get('confirm_password')?.value;
      return pass === confirm ? null : { notSame: true };
    }
  });

  onSubmit() {
    if (this.registerForm.valid) {
      // Envía TODO el formulario, no hagas destructuring para excluir campos
      const userData = this.registerForm.getRawValue();

      this.authService.register(userData).subscribe({
        next: () => {
          this.successMessage = '¡Registro exitoso!';
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: (err) => {
          console.error('Error detallado:', err.error);
          this.errorMessage = 'Error en el registro. Revisa los campos.';
        }
      });
    } else {
      this.errorMessage = 'Formulario inválido. Revisa las validaciones.';
    }
  }
}