FROM node:18.19.0-buster-slim

WORKDIR /fba_ui

COPY . .

RUN rm -rf node_modules
RUN npm --registry https://registry.npmmirror.com install -g pnpm
RUN pnpm config set registry https://registry.npmmirror.com \
    && pnpm install
