import { Routes } from '@angular/router';
import { Login } from '../app/modules/auth/login/login';
import { Register } from '../app/modules/auth/register/register';
// Importamos el componente principal del Dashboard
import { Dashboard } from './modules/dashboard/dashboard';
import { MapaRiesgo } from './modules/dashboard/mapa-riesgo/mapa-riesgo';
import { KpiCards } from './modules/dashboard/kpi-cards/kpi-cards';
import { TablaRanking } from './modules/dashboard/tabla-ranking/tabla-ranking';
import { GraficoTendencias } from './modules/dashboard/grafico-tendencias/grafico-tendencias';
import { DetallePais } from './modules/paises/detalle-pais/detalle-pais'
import { Portafolios } from './modules/portafolios/portafolios'
export const routes: Routes = [
    { path: 'login', component: Login },
    { path: 'register', component: Register },

    // Nueva ruta para el Dashboard
    { path: 'dashboard', component: Dashboard },
    {
        path: 'dashboard',
        component: Dashboard,
        children: [
            { path: 'app-mapa-riesgo', component: MapaRiesgo },
            { path: 'app-kpi-cards', component: KpiCards },
            { path: 'app-kpi-cards', component: TablaRanking },
            { path: 'app-kpi-cards', component: TablaRanking },
            { path: 'app-grafico-tendencias', component: GraficoTendencias },
        ]
    },
    { path: 'detalle-pais', component: DetallePais },
    { path: 'app-portafolios', component: Portafolios },
    // Redirecciones
    { path: '', redirectTo: 'app-portafolios', pathMatch: 'full' },
    { path: '**', redirectTo: 'app-portafolios' }
];