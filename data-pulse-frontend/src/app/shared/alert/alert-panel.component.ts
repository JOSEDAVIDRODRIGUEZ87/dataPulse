import { Component, inject, signal, computed } from '@angular/core';
import { AlertService } from '../../../app/core/services/alerta.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-alert-panel',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="p-3">
      <div class="d-flex justify-content-between mb-3">
        <h3>Alertas</h3>
        <button class="btn btn-outline-primary btn-sm" (click)="srv.marcarTodasLeidas()">Marcar todas leídas</button>
      </div>

      @for (a of alertasFiltradas(); track a.id) {
        <div class="alert" [ngClass]="getClaseSeveridad(a.severidad)" [class.opacity-50]="a.leida">
          <i class="bi bi-bell"></i> {{ a.mensaje }}
          @if (!a.leida) { <button class="btn-close" (click)="srv.marcarLeida(a.id)"></button> }
        </div>
      }
    </div>
  `
})
export class AlertPanel {
    srv = inject(AlertService);
    filtroSeveridad = signal<string>('todas');

    alertasFiltradas = computed(() => {
        return this.filtroSeveridad() === 'todas'
            ? this.srv.alertas()
            : this.srv.alertas().filter(a => a.severidad === this.filtroSeveridad());
    });

    getClaseSeveridad(sev: string): string {
        switch (sev) {
            case 'alta': return 'alert-danger';
            case 'media': return 'alert-warning';
            default: return 'alert-info';
        }
    }
}