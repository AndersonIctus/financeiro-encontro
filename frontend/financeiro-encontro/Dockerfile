FROM node:20 as build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build --prod

FROM nginx:alpine

COPY --from=build /app/dist/financeiro-encontro /usr/share/nginx/html
