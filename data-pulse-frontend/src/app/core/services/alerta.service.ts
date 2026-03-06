import { Injectable, signal, computed } from '@angular/core';
import { Alerta } from '../../../models/alerta.model';
import { interval } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AlertService {
  private _alertas = signal<Alerta[]>([]);
  public alertas = this._alertas.asReadonly();

  // Conteo reactivo para el Badge del Navbar
  public noLeidasCount = computed(() => this._alertas().filter(a => !a.leida).length);

  constructor() {
    // Polling cada 30 segundos (30000 ms)
    interval(30000).subscribe(() => this.simularNuevaAlerta());
  }

  private simularNuevaAlerta() {
    const nueva: Alerta = {
      id: Date.now(),
      mensaje: 'Notificación de mercado detectada',
      tipo: 'mercado',
      severidad: 'media',
      leida: false,
      fecha: new Date()
    };
    this._alertas.update(list => [nueva, ...list]);
  }

  marcarLeida(id: number) {
    this._alertas.update(list => list.map(a => a.id === id ? { ...a, leida: true } : a));
  }

  marcarTodasLeidas() {
    this._alertas.update(list => list.map(a => ({ ...a, leida: true })));
  }
}