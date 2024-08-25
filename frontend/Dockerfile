FROM node:18.19.0-buster-slim AS build

WORKDIR /fba_ui

COPY . .

RUN rm -rf node_modules
RUN npm --registry https://registry.npmmirror.com install -g pnpm
RUN pnpm config set registry https://registry.npmmirror.com \
    && pnpm install && pnpm run build

FROM nginx

COPY ./deploy/nginx.conf /etc/nginx/nginx.conf

COPY --from=build /fba_ui/dist /www/fba_ui

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
