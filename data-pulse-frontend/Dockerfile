# Usamos una versión estable de Node
FROM node:20-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias primero para aprovechar el caché de Docker
COPY package*.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos todo el código fuente al contenedor
COPY . .

# Exponemos el puerto de Angular
EXPOSE 4200

# Comando para iniciar el servidor de desarrollo
# El host 0.0.0.0 es necesario para que sea accesible desde afuera del contenedor
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "1"]