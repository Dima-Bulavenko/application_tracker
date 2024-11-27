FROM node:23-alpine3.19

WORKDIR /code

COPY package*.json ./

RUN npm install

COPY ./ /code/

CMD ["npm", "start"]
