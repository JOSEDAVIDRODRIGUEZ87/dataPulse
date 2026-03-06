import { Component, EventEmitter, Input, OnInit, Output, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule, AbstractControl, ValidationErrors, AsyncValidatorFn } from '@angular/forms';
import { Portafolio } from '../../../../models/portafolio.model';
import { PortafolioService } from '../../../core/services/portafolio.service'; // Ajusta la ruta a tu servicio
import { debounceTime, map, catchError, of, Observable } from 'rxjs';
@Component({
  selector: 'app-crear',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './crear.html'
})
export class Crear implements OnInit {
  @Input() portafolioEditar?: Portafolio;
  @Output() save = new EventEmitter<Portafolio>();
  @Output() cancelar = new EventEmitter<void>();
  private svc = inject(PortafolioService); // Inyectamos el servicio para la validación async

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(100)], [this.nombreUnicoValidator()]],
      descripcion: ['', [Validators.maxLength(500)]], // <--- IMPORTANTE
      esPublico: [false],
      posiciones: this.fb.array([])
    });
  }

  get posiciones() { return this.form.get('posiciones') as FormArray; }

  ngOnInit() {
    if (this.portafolioEditar) {
      this.form.patchValue({
        nombre: this.portafolioEditar.nombre,
        esPublico: this.portafolioEditar.esPublico
      });

      // Limpiamos el array antes de rellenar
      this.posiciones.clear();

      // Rellenamos el FormArray correctamente
      this.portafolioEditar.posiciones.forEach(p => {
        this.posiciones.push(this.fb.group({
          pais: [p.pais, Validators.required],
          tipo_activo: [p.tipoActivo, Validators.required],
          monto: [p.monto, [Validators.required, Validators.min(0)]],
          riesgo: [p.riesgo || 0, Validators.required]
        }));
      });
    }
  }

  agregarPosicion() {
    const nuevaPos = this.fb.group({
      pais: ['', Validators.required],
      tipo_activo: ['Acción', Validators.required],
      monto: [0, [Validators.required, Validators.min(0)]],
      riesgo: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]]
    });
    this.posiciones.push(nuevaPos);
  }

  // En onSubmit()
  onSubmit() {
    if (this.form.valid) {
      const nuevoPortafolio: Portafolio = {
        ...this.portafolioEditar,
        ...this.form.value,
        // Generamos un ID numérico simple (basado en tiempo para evitar colisiones)
        id: this.portafolioEditar?.id ?? Math.floor(Math.random() * 1000000)
      };
      this.save.emit(nuevoPortafolio);
    }
  }
  nombreUnicoValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return this.svc.verificarNombreUnico(control.value).pipe(
        debounceTime(500), // Evita saturar el backend mientras escribe
        map(esUnico => (esUnico ? null : { nombreDuplicado: true })),
        catchError(() => of(null))
      );
    };
  }
}