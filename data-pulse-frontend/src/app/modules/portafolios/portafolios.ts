import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common'; // Necesario para *ngIf
import { Portafolio } from '../../../models/portafolio.model';
import { Posicion } from '../../../models/posicion.model';
import { Lista } from './lista/lista'; // Ajusta la ruta
import { Crear } from './crear/crear';     // Ajusta la ruta
import { GraficoTendencias } from '../../modules/dashboard/grafico-tendencias/grafico-tendencias'; 

@Component({
  selector: 'app-portafolios',
  standalone: true, // Asegúrate que sea standalone
  imports: [CommonModule, Lista, Crear,GraficoTendencias],
  templateUrl: './portafolios.html',
  styleUrl: './portafolios.scss',
})
export class Portafolios {
  // Estado del flujo
  modoVista: 'LISTAR' | 'FORMULARIO' = 'LISTAR';
  portafolioAEditar?: Portafolio;

  // Tu lógica de estado actual
  portafolios = signal<Portafolio[]>([]);
  posicionesSeleccionadas = signal<Posicion[]>([]);

  // Cálculos en tiempo real
  totalInvertido = computed(() => this.posicionesSeleccionadas().reduce((acc, p) => acc + p.monto, 0));

  riesgoPromedio = computed(() => {
    const total = this.totalInvertido();
    return total > 0 ? (this.posicionesSeleccionadas().reduce((acc, p) => acc + (p.monto * p.riesgo), 0) / total).toFixed(2) : 0;
  });

  // Métodos de navegación
  abrirCrear() {
    this.portafolioAEditar = undefined;
    this.modoVista = 'FORMULARIO';
  }

  abrirEditar(p: Portafolio) {
    this.portafolioAEditar = p;
    this.modoVista = 'FORMULARIO';
  }

  // En portafolios.ts
  guardarPortafolio(portafolio: Portafolio) {
    this.portafolios.update(lista => {
      const index = lista.findIndex(p => p.id === portafolio.id);

      if (index !== -1) {
        // ESTO ES EDITAR: reemplazamos el elemento en el índice encontrado
        const nuevaLista = [...lista];
        nuevaLista[index] = portafolio;
        return nuevaLista;
      } else {
        // ESTO ES CREAR: agregamos al final
        return [...lista, portafolio];
      }
    });

    this.modoVista = 'LISTAR'; // Volvemos al listado
  }
}