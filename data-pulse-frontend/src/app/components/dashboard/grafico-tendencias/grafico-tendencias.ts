import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';

@Component({
  selector: 'app-grafico-tendencias',
  standalone: true,
  imports: [CommonModule, FormsModule,BaseChartDirective],
  templateUrl: './grafico-tendencias.html',
  styleUrls: ['./grafico-tendencias.scss']
})
export class GraficoTendencias {
  // Configuración de los datos
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [82, 84, 83, 85, 85],
        label: 'Uruguay',
        backgroundColor: 'rgba(25, 135, 84, 0.1)',
        borderColor: '#198754',
        pointBackgroundColor: '#198754',
        fill: 'origin',
      },
      {
        data: [70, 72, 68, 71, 71],
        label: 'México',
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        borderColor: '#0d6efd',
        pointBackgroundColor: '#0d6efd',
        fill: 'origin',
      },
      {
        data: [40, 42, 45, 43, 45],
        label: 'Argentina',
        backgroundColor: 'rgba(220, 53, 69, 0.1)',
        borderColor: '#dc3545',
        pointBackgroundColor: '#dc3545',
        fill: 'origin',
      }
    ],
    labels: ['2021', '2022', '2023', '2024', '2025']
  };

  public lineChartOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'top' },
    },
    scales: {
      y: { min: 0, max: 100, title: { display: true, text: 'Puntaje IRPC' } }
    }
  };

  public lineChartType: ChartType = 'line';
}