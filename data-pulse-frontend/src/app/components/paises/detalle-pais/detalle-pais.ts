import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-detalle-pais',
  imports: [CommonModule, BaseChartDirective],
  standalone: true,
  templateUrl: './detalle-pais.html',
  styleUrl: './detalle-pais.scss',
})

export class DetallePais implements OnInit {
  paisNombre = "México"; // Esto vendría de ActivatedRoute

  // 1. Gráfico Histórico Indicadores (5 años)
  public historicalData: ChartConfiguration['data'] = {
    datasets: [
      { data: [65, 68, 70, 69, 71], label: 'IRPC', borderColor: '#0d6efd', fill: true },
      { data: [4.5, 5.2, 7.8, 6.1, 4.8], label: 'Inflación %', borderColor: '#dc3545' }
    ],
    labels: ['2021', '2022', '2023', '2024', '2025']
  };

  // 2. Histórico Tipo de Cambio (30 días)
  public currencyData: ChartConfiguration['data'] = {
    datasets: [{
      data: [19.8, 20.1, 19.9, 20.3, 19.5, 18.9, 19.1], // Simulado
      label: 'MXN / USD',
      borderColor: '#198754',
      tension: 0.4
    }],
    labels: ['Día 1', 'Día 5', 'Día 10', 'Día 15', 'Día 20', 'Día 25', 'Día 30']
  };

  public chartOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false
  };

  constructor() { }
  ngOnInit(): void { }
}