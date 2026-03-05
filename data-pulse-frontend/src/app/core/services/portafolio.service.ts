import { Injectable, signal } from '@angular/core';
import { Portafolio } from '../../../models/portafolio.model';

@Injectable({ providedIn: 'root' })
export class PortafolioService {
  portafolios = signal<Portafolio[]>(JSON.parse(localStorage.getItem('portafolios') || '[]'));

  guardar(p: Portafolio) {
    const lista = [...this.portafolios()];
    const idx = lista.findIndex(i => i.id === p.id);
    if (idx > -1) lista[idx] = p; else lista.push(p);
    this.portafolios.set(lista);
    localStorage.setItem('portafolios', JSON.stringify(lista));
  }

  eliminar(id: number) {
    this.portafolios.update(list => list.filter(p => p.id !== id));
    localStorage.setItem('portafolios', JSON.stringify(this.portafolios()));
  }
}