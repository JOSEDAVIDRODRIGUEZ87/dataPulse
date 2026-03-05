import { Posicion } from './posicion.model'; // Importamos la interfaz independiente

export interface Portafolio {
    id: number;
    nombre: string;
    esPublico: boolean;
    posiciones: Posicion[]; // Composición: un portafolio tiene un array de posiciones
}