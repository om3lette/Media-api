FROM node:24-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --silent

COPY . .

RUN npm run build

FROM nginx
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend.conf.template /etc/nginx/conf.d/default.conf
