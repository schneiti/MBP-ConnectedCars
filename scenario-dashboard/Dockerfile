FROM node:16
WORKDIR /usr/src/app
COPY package*.json ./
RUN export SET NODE_OPTIONS=--openssl-legacy-provider
RUN npm install

COPY . .
EXPOSE 8081
CMD ["npm", "run", "serve"]