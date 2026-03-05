import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-mapa-riesgo',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mapa-riesgo.html',
  styleUrls: ['./mapa-riesgo.scss']
})
export class MapaRiesgo { // Verifica que el nombre de la clase sea exactamente este
  datosPaises: any = {
    'AR': { nombre: 'Argentina', irpc: 45 },
    'BR': { nombre: 'Brasil', irpc: 68 },
    'CL': { nombre: 'Chile', irpc: 82 },
    'CO': { nombre: 'Colombia', irpc: 62 },
    'MX': { nombre: 'México', irpc: 71 },
    'PE': { nombre: 'Perú', irpc: 58 },
    'UY': { nombre: 'Uruguay', irpc: 85 }
  };

  tooltipNombre: string = 'Selecciona un país';
  tooltipValor: string = '0';

  // ESTA ES LA FUNCIÓN QUE FALTABA
  getTooltipBadgeColor(): string {
    const valor = parseInt(this.tooltipValor);
    if (isNaN(valor) || valor === 0) return '#6c757d'; // Gris si no hay selección
    if (valor >= 80) return '#198754'; // Verde (Bajo Riesgo)
    if (valor >= 60) return '#ffc107'; // Amarillo (Riesgo Medio)
    return '#dc3545';               // Rojo (Riesgo Crítico)
  }

  getPaisColor(iso: string): string {
    const val = this.datosPaises[iso]?.irpc || 0;
    if (val >= 80) return '#198754';
    if (val >= 60) return '#ffc107';
    if (val > 0) return '#dc3545';
    return '#e9ecef'; // Color por defecto para países sin datos
  }

  mostrarInfo(iso: string) {
    if (this.datosPaises[iso]) {
      this.tooltipNombre = this.datosPaises[iso].nombre;
      this.tooltipValor = this.datosPaises[iso].irpc.toString();
    }
  }
}