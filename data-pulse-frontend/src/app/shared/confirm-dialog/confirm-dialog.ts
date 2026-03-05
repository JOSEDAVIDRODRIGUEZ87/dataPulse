import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [MatButtonModule, MatDialogModule],
  template: `
    <h2 mat-dialog-title>Confirmación</h2>
    <mat-dialog-content>
      {{ data.mensaje }}
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="dialogRef.close(false)">Cancelar</button>
      <button mat-button color="warn" (click)="dialogRef.close(true)">Eliminar</button>
    </mat-dialog-actions>
  `
})
export class ConfirmDialog {
  constructor(
    // El token de inyección es la propia clase MatDialogRef
    public dialogRef: MatDialogRef<ConfirmDialog>,
    // El token de datos DEBE ir con @Inject
    @Inject(MAT_DIALOG_DATA) public data: { mensaje: string }
  ) { }
}