## build args
FROM node:16-alpine as build-deps
WORKDIR /app
COPY ./ui/package.json /app
COPY ./ui/yarn.lock /app
RUN yarn install
COPY ./ui /app
# cat .env.production
RUN yarn build

## production
FROM nginx:1.19-alpine

WORKDIR /usr/share/nginx/html
RUN apk add --no-cache bash

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-deps /app/build .
EXPOSE 80
CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]