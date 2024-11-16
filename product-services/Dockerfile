FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN apt-get update && apt-get install -y wait-for-it
COPY . .
EXPOSE 3000
CMD ["wait-for-it", "product-db:3306", "--timeout=60", "--", "node", "app.js"]