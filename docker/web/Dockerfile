FROM node:lts-alpine as builder

WORKDIR /app

ENV NODE_ENV production

ARG SENTRY_DSN
ARG SOURCE_COMMIT

ENV SENTRY_DSN $SENTRY_DSN
ENV SOURCE_COMMIT $SOURCE_COMMIT

COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn YARN_CACHE_FOLDER=/root/.yarn yarn install --production --ignore-optional --frozen-lockfile

COPY ./frontend ./frontend
COPY ./nuxt.config.js ./
COPY ./.sentryclirc ./.sentryclirc

RUN yarn build

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/web/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
