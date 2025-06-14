# Stage 1: Build the Angular application
FROM node:12 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.27.5-alpine

# TODO: what is this for?
# COPY nginx.tmpl /etc/nginx/templates/default.conf.template

COPY --from=builder /app/dist/frontend/ /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
