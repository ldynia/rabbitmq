#!/usr/bin/env sh

# Install dependencies
apk upgrade && apk add \
    git \
    make \
    openssl

# Clone tls-gen repository
git clone https://github.com/rabbitmq/tls-gen.git /tmp/tls-gen
cd /tmp/tls-gen/basic

# Generate certificates. CN value MUST be the hostname of the broker service
make CN=rabbitmq-broker
make CN=rabbitmq-broker alias-leaf-artifacts

# Copy certificates and fix permissions
mv result/ca_certificate.pem \
    result/ca_key.pem \
    result/client_certificate.pem \
    result/client_key.pem \
    result/server_certificate.pem \
    result/server_key.pem \
    /etc/ssl/private
chmod -R 444 /etc/ssl/private/*
