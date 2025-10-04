# 1. Build stage - use Node to build React app
FROM node:20-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# 2. Serve stage - use Nginx for static hosting
FROM nginx:alpine

# copy built React app from build stage to Nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
