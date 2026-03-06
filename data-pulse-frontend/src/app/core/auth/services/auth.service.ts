import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { AuthResponse } from '../../../../models/auth.models';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private readonly TOKEN_KEY = 'data_pulse_token';

  // El BehaviorSubject mantiene el estado del usuario en memoria mientras la app está abierta
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor() {
    // Al cargar la app, revisamos si ya había una sesión guardada
    const savedToken = localStorage.getItem(this.TOKEN_KEY);
    if (savedToken) {
      // Aquí podrías decodificar el token o pedir los datos del usuario al servidor
      this.currentUserSubject.next({ token: savedToken });
    }
  }

  login(credentials: { email: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${environment.apiUrl}/auth/login/`, credentials).pipe(
      tap(response => {
        // Guardar ambos tokens para permitir la renovación automática
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  // REGISTRO: Crea un nuevo usuario
  register(userData: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/auth/register/`, userData);
  }

  // LOGOUT: Limpia todo y cierra sesión
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    this.currentUserSubject.next(null);
  }

  // Helper para obtener el token rápidamente (útil para el Interceptor)
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }
}