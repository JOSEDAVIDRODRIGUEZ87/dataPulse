export interface AuthResponse {
    access: string;
    refresh: string;
    user: {
        id: number;
        nombre_completo: string;
        email: string;
        rol: string;
    };
}