FROM node:alpine

WORKDIR /usr/src/app/my-app

COPY package*.json ./

RUN npm install

CMD ["npm", "run", "dev"]