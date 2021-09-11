FROM node:lts-alpine as builder

WORKDIR /app

ENV NODE_ENV production

COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci

COPY ./assets ./assets
COPY ./components ./components
COPY ./assets ./assets
COPY ./layouts ./layouts
COPY ./middleware ./middleware
COPY ./pages ./pages
COPY ./plugins ./plugins
COPY ./static ./static
COPY ./store ./store
COPY ./nuxt.config.js ./

RUN yarn build

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/web/nginx.conf /etc/nginx/conf.d
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
