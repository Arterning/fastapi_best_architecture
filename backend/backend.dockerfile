FROM fba-base

COPY . .

WORKDIR /

RUN mv fba backend && mkdir -p /var/log/fastapi_server && mv /backend/.env.server /backend/.env

COPY deploy/fastapi_server.conf /etc/supervisor/conf.d/

EXPOSE 8000