import { Injectable, signal } from '@angular/core';
import { Alerta } from '../../../models/alerta.model';

@Injectable({ providedIn: 'root' })
export class Alert {
  alertas = signal<Alerta[]>([]);

  agregar(alerta: Alerta) {
    this.alertas.update(prev => [alerta, ...prev]);
  }
}
