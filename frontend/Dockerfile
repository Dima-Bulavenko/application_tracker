FROM node:23-alpine3.19 AS install

WORKDIR /code

COPY package*.json ./

RUN npm install

COPY . .


# Commands for build
FROM install AS build

RUN npm run build


# Command for production
FROM nginx:1.27.3-alpine AS production

COPY --from=build /code/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
