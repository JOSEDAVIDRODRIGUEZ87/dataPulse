export interface Alerta {
    id: number;
    mensaje: string;
    tipo: 'inversion' | 'sistema' | 'mercado';
    severidad: 'baja' | 'media' | 'alta';
    leida: boolean;
    fecha: Date;
}