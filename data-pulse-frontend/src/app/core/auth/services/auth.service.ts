import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../../environments/environment';

// Definimos qué estructura esperamos de Django
interface AuthResponse {
  access: string;
  refresh: string;
  user: {
    username: string;
    email: string;
    role: string;
  };
}

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

  // LOGIN: Envía credenciales y guarda el token si es exitoso
  login(credentials: { username: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${environment.apiUrl}/users/login/`, credentials).pipe(
      tap(response => {
        localStorage.setItem(this.TOKEN_KEY, response.access);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  // REGISTRO: Crea un nuevo usuario
  register(userData: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/users/register/`, userData);
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