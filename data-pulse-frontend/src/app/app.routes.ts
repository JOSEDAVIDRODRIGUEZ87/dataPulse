import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: 'login',
        loadComponent: () => import('./components/auth/login/login').then(m => m.Login)
    },
    {
        path: 'register',
        loadComponent: () => import('./components/auth/register/register').then(m => m.Register)
    },

    // Dashboard con Lazy Loading y Rutas Hijas
    {
        path: 'dashboard',
        loadComponent: () => import('./components/dashboard/dashboard').then(m => m.Dashboard),
        children: [
            { path: 'mapa-riesgo', loadComponent: () => import('./components/dashboard/mapa-riesgo/mapa-riesgo').then(m => m.MapaRiesgo) },
            { path: 'kpi-cards', loadComponent: () => import('./components/dashboard/kpi-cards/kpi-cards').then(m => m.KpiCards) },
            { path: 'ranking', loadComponent: () => import('./components/dashboard/tabla-ranking/tabla-ranking').then(m => m.TablaRanking) },
            { path: 'tendencias', loadComponent: () => import('./components/dashboard/grafico-tendencias/grafico-tendencias').then(m => m.GraficoTendencias) },
        ]
    },
    {
        path: 'detalle-pais',
        loadComponent: () => import('./components/paises/detalle-pais/detalle-pais').then(m => m.DetallePais)
    },
    {
        path: 'portafolios',
        loadComponent: () => import('./components/portafolios/portafolios').then(m => m.Portafolios)
    },

    { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    { path: '**', redirectTo: 'dashboard' }
];