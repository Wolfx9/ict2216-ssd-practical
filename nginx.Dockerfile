FROM nginxinc/nginx-unprivileged:alpine

USER root
RUN apk add --no-cache openssl \
    && mkdir -p /etc/nginx/certs \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
         -keyout /etc/nginx/certs/server.key \
         -out /etc/nginx/certs/server.crt \
         -subj "/C=SG/ST=Singapore/L=Singapore/O=SIT/OU=ICT2216/CN=localhost" \
         -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" \
    && chown -R nginx:nginx /etc/nginx/certs
USER nginx
