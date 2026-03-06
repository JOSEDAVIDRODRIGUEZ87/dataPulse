import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface PaisRanking {
  nombre: string;
  irpc: number;
  variacion: string;
  tendencia: 'up' | 'down' | 'stable';
}

@Component({
  selector: 'app-tabla-ranking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tabla-ranking.html',
  styleUrls: ['./tabla-ranking.scss']
})
export class TablaRanking implements OnInit {
  ranking: PaisRanking[] = [
    { nombre: 'Uruguay', irpc: 85, variacion: '+1.2%', tendencia: 'up' },
    { nombre: 'Chile', irpc: 82, variacion: '+0.5%', tendencia: 'up' },
    { nombre: 'Costa Rica', irpc: 78, variacion: '-0.2%', tendencia: 'down' },
    { nombre: 'Panamá', irpc: 72, variacion: '0.0%', tendencia: 'stable' },
    { nombre: 'México', irpc: 71, variacion: '+0.8%', tendencia: 'up' },
    { nombre: 'Brasil', irpc: 68, variacion: '-1.5%', tendencia: 'down' },
    { nombre: 'Colombia', irpc: 62, variacion: '+0.3%', tendencia: 'up' },
    { nombre: 'Perú', irpc: 58, variacion: '-2.1%', tendencia: 'down' },
    { nombre: 'Ecuador', irpc: 52, variacion: '-0.7%', tendencia: 'down' },
    { nombre: 'Argentina', irpc: 45, variacion: '+3.2%', tendencia: 'up' }
  ];

  constructor() { }

  ngOnInit(): void {
    // Ordenamos por IRPC de mayor a menor por si acaso
    this.ranking.sort((a, b) => b.irpc - a.irpc);
  }

  getNivelRiesgo(irpc: number): string {
    if (irpc >= 80) return 'Bajo';
    if (irpc >= 60) return 'Medio';
    return 'Alto';
  }

  getClaseNivel(irpc: number): string {
    if (irpc >= 80) return 'text-success bg-success-subtle';
    if (irpc >= 60) return 'text-warning bg-warning-subtle';
    return 'text-danger bg-danger-subtle';
  }
}