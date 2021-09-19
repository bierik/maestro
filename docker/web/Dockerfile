FROM node:lts-alpine as builder

WORKDIR /app

ENV NODE_ENV production

ARG SENTRY_DSN
ARG SOURCE_COMMIT

ENV SENTRY_DSN $SENTRY_DSN
ENV SOURCE_COMMIT $SOURCE_COMMIT

COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn YARN_CACHE_FOLDER=/root/.yarn yarn install --production --ignore-optional --frozen-lockfile

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
COPY ./.sentryclirc ./.sentryclirc

RUN yarn build

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/web/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
