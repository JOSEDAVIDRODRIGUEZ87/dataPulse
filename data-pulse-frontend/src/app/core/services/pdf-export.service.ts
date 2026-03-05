import { Injectable } from '@angular/core';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';
import { Posicion } from '../../../models/posicion.model'; // Asegura el tipo correcto

@Injectable({
    providedIn: 'root',
})
export class PdfExportService {

    exportar(posiciones: Posicion[], nombrePortafolio: string) {
        const doc = new jsPDF();

        // Configuración de estilo
        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);
        doc.text(`Reporte: ${nombrePortafolio}`, 14, 20);

        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        doc.text(`Generado el: ${new Date().toLocaleDateString()}`, 14, 28);

        // Tabla con estilo DataPulse
        (doc as any).autoTable({
            startY: 35,
            head: [['País', 'Tipo de Activo', 'Monto (USD)']],
            body: posiciones.map(p => [p.pais, p.tipoActivo, p.monto.toLocaleString()]),
            headStyles: { fillColor: [13, 110, 253] }, // Azul corporativo (Bootstrap primary)
            alternateRowStyles: { fillColor: [240, 240, 240] }
        });

        doc.save(`portafolio_${nombrePortafolio.toLowerCase().replace(/\s/g, '_')}.pdf`);
    }
}