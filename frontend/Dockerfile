FROM node:15 AS builder

ARG API_URL=http://localhost:8000

WORKDIR /app

COPY package.json .

# Does not take in account the version used for local development
# This is dangerous as it may lead to unexpected code behavior in production
# This is a temporarry hack and it should be fixed as soon as possible
# COPY package-lock.json .

RUN npm install

# TODO make the react configuration work
COPY .env .
COPY .env.production.template .
RUN sed -e "s|PLACEHOLDER_API_URL|${API_URL}|g" < .env.production.template  > .env.production

# Copy the sources and the content
COPY src/ src/
COPY public/ public/

RUN npm run build

FROM nginx:latest

EXPOSE 80
COPY --from=builder /app/build/ /usr/share/nginx/html
