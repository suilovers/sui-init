## build args
FROM node:16-alpine as build-deps
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn install
COPY . ./
# cat .env.production
RUN yarn build

## production
FROM nginx:1.19-alpine

WORKDIR /usr/share/nginx/html
COPY ./env.sh .
COPY .env .
RUN apk add --no-cache bash
RUN chmod +x env.sh

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-deps /usr/src/app/build .
EXPOSE 80
CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]