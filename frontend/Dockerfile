# Usamos una versión ligera de Node.js
FROM node:22-slim

# Creamos la carpeta de trabajo
WORKDIR /app

# Copiamos los archivos de configuración y descargamos dependencias
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copiamos el resto de tu código Vue
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Encendemos el servidor de Vue (el --host es vital para que Docker lo exponga)
CMD ["npm", "run", "dev", "--", "--host"]