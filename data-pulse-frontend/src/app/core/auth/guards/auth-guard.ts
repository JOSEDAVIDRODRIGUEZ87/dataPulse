import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.getToken()) {
    return true; // Adelante, tiene token
  }

  // Si no hay token, lo mandamos de patitas a la calle (al login)
  router.navigate(['/login']);
  return false;
};