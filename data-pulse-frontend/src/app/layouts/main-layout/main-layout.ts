import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; // Necesario para router-outlet
import { Navbar } from '../../components/navbar/navbar'; // Ajusta la ruta a donde esté tu Navbar

@Component({
  selector: 'app-main-layout',
  imports: [RouterModule,
    Navbar],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss',
})
export class MainLayout { }
