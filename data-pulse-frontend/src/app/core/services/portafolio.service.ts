import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Portafolio } from '../../../models/portafolio.model';
import { Observable, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PortafolioService {
  private http = inject(HttpClient);
  private API_URL = 'https://api.datapulse.com/portafolios'; // Tu endpoint real

  // Señal que mantiene el estado actual
  portafolios = signal<Portafolio[]>([]);

  // 1. Cargar datos desde Backend (Ejecutar al iniciar)
  cargarPortafolios(): Observable<Portafolio[]> {
    return this.http.get<Portafolio[]>(this.API_URL).pipe(
      tap(data => this.portafolios.set(data))
    );
  }

  // 2. Guardar (POST/PUT con manejo de estado optimista)
  guardar(p: Portafolio): Observable<Portafolio> {
    return this.http.post<Portafolio>(this.API_URL, p).pipe(
      tap(nuevoP => {
        this.portafolios.update(lista => [...lista, nuevoP]);
      })
    );
  }

  // 3. Validación Asíncrona (Requisito técnico 2.4)
  verificarNombreUnico(nombre: string): Observable<boolean> {
    return this.http.get<boolean>(`${this.API_URL}/check-name?nombre=${nombre}`);
  }
}