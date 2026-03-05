import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
// Importa los subcomponentes que acabas de crear
import { KpiCards } from './kpi-cards/kpi-cards';
import { GraficoTendencias } from './grafico-tendencias/grafico-tendencias';
import { TablaRanking } from './tabla-ranking/tabla-ranking';
import { MapaRiesgo } from './mapa-riesgo/mapa-riesgo';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    //RouterOutlet, // 2. Agrégalo aquí para que reconozca <router-outlet>
    RouterModule, // Opcional: Agrégalo si también usas [routerLink]
    KpiCards,
    GraficoTendencias,
    TablaRanking,
    MapaRiesgo
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class Dashboard { }