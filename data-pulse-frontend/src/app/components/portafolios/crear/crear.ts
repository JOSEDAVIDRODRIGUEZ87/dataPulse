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
      descripcion: ['', [Validators.maxLength(500)]],
      esPublico: [false],
      // AÑADIMOS EL VALIDADOR AQUÍ:
      posiciones: this.fb.array([], this.posicionesValidator.bind(this))
    });
  }

  get posiciones() { return this.form.get('posiciones') as FormArray; }

  // Validación de fecha para que no sea futura
  fechaNoFuturaValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) return null;
    const fechaSeleccionada = new Date(control.value);
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    return fechaSeleccionada > hoy ? { fechaFutura: true } : null;
  }

  ngOnInit() {
    if (this.portafolioEditar) {
      this.form.patchValue({
        nombre: this.portafolioEditar.nombre,
        //descripcion: this.portafolioEditar.descripcion,
        esPublico: this.portafolioEditar.esPublico
      });

      // Limpiamos el array antes de rellenar
      this.posiciones.clear();

      // Rellenamos el FormArray correctamente
      this.portafolioEditar.posiciones.forEach(p => {
        this.posiciones.push(this.fb.group({
          pais: [p.pais, Validators.required],
          tipo_activo: [p.tipoActivo, Validators.required],
          monto: [p.monto, [Validators.required, Validators.min(1000), Validators.max(10000000)]],
          // fechaEntrada: [p.fechaEntrada, [Validators.required, this.fechaNoFuturaValidator]],
          riesgo: [p.riesgo || 0, Validators.required]
        }));
      });
    }
  }

  agregarPosicion() {
    const nuevaPos = this.fb.group({
      pais: ['', Validators.required],
      tipo_activo: ['Acción', Validators.required],
      monto: [1000, [Validators.required, Validators.min(1000), Validators.max(10000000)]],
      fechaEntrada: ['', [Validators.required, this.fechaNoFuturaValidator]],
      notas: ['', Validators.maxLength(200)]
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
  // En tu clase Crear:
  posicionesValidator(control: AbstractControl): ValidationErrors | null {
    const formArray = control as FormArray;
    const posiciones = formArray.controls;
    let montoTotal = 0;

    posiciones.forEach((pos, index) => {
      const valor = pos.value;
      montoTotal += (valor.monto || 0);

      // Regla 1: No MONEDA si el país es 'EE.UU.' (suponiendo que EE.UU. es el país USD)
      if (valor.pais === 'EE.UU.' && valor.tipo_activo === 'MONEDA') {
        pos.setErrors({ errorMonedaUsd: true });
      }

      // Regla 3: No más de 2 posiciones del mismo tipo en el mismo país
      const duplicados = posiciones.filter(item =>
        item.value.pais === valor.pais && item.value.tipo_activo === valor.tipo_activo
      );
      if (duplicados.length > 2) {
        pos.setErrors({ limiteTipoPais: true });
      }
    });

    // Regla 2: Monto total <= 50,000,000
    if (montoTotal > 50000000) {
      return { limiteMontoGlobal: true };
    }

    return null;
  }
}