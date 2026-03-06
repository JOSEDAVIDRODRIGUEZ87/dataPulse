import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Portafolio } from '../../../../models/portafolio.model';
import jsPDF from 'jspdf'; // Importación necesaria

@Component({
  selector: 'app-lista',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './lista.html',
  styleUrl: './lista.scss',
})
export class Lista {
  @Input() portafolios: Portafolio[] = [];
  @Output() crear = new EventEmitter<void>();
  @Output() editar = new EventEmitter<Portafolio>();
  @Output() eliminar = new EventEmitter<number>();

  onEditar(p: Portafolio) { this.editar.emit(p); }

  onEliminar(id: number) {
    if (confirm('¿Estás seguro de eliminar este portafolio?')) {
      this.eliminar.emit(id);
    }
  }

  // Lógica para exportar a PDF
  exportarPDF(p: Portafolio) {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text(`Portafolio: ${p.nombre}`, 10, 10);
    doc.setFontSize(10);
    p.posiciones.forEach((pos, i) => {
      doc.text(`${i + 1}. ${pos.pais} - ${pos.tipoActivo}: $${pos.monto}`, 10, 20 + (i * 10));
    });
    doc.save(`${p.nombre.replace(/\s+/g, '_')}.pdf`);
  }
}