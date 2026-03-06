import { Component, inject } from '@angular/core';
import { AlertService } from '../../core/services/alerta.service'; // Ajusta la ruta según donde lo hayas guardado

@Component({
  selector: 'app-navbar',
  standalone: true,
  styleUrl: './navbar.scss',
  templateUrl: './navbar.html',
})
export class Navbar {
  alertSrv = inject(AlertService);
}