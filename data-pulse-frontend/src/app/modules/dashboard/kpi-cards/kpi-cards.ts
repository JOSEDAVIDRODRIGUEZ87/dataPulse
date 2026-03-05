import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kpi-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kpi-cards.html',
  styleUrls: ['./kpi-cards.scss']
})
export class KpiCards {
  kpis = [
    {
      title: 'Países Monitoreados',
      value: '18',
      icon: 'bi-globe-americas',
      color: 'primary',
      trend: '+2 este mes'
    },
    {
      title: 'Alertas Activas',
      value: '05',
      icon: 'bi-exclamation-triangle',
      color: 'danger',
      trend: '3 críticas'
    },
    {
      title: 'Portafolios Usuario',
      value: '12',
      icon: 'bi-briefcase',
      color: 'info',
      trend: 'Actualizado hoy'
    },
    {
      title: 'Promedio IRPC Región',
      value: '64.2',
      icon: 'bi-graph-up-arrow',
      color: 'success',
      trend: 'Estable'
    }
  ];
}