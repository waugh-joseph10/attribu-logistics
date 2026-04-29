#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}SSL Certificate Setup Script${NC}"
echo "This script will obtain Let's Encrypt SSL certificates for your domain."
echo ""

# Prompt for domain
read -p "Enter your primary domain (e.g., attribu.io): " DOMAIN
read -p "Enter your www domain (e.g., www.attribu.io) or press Enter to skip: " WWW_DOMAIN
read -p "Enter your email address: " EMAIL

# Validate inputs
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo -e "${RED}Error: Domain and email are required${NC}"
    exit 1
fi

# Create certbot directories
echo -e "${YELLOW}Creating certbot directories...${NC}"
mkdir -p certbot/conf certbot/www

# Build domain arguments
DOMAIN_ARGS="-d $DOMAIN"
if [ ! -z "$WWW_DOMAIN" ]; then
    DOMAIN_ARGS="$DOMAIN_ARGS -d $WWW_DOMAIN"
fi

echo -e "${YELLOW}Starting nginx for certificate verification...${NC}"
docker compose up -d nginx

# Wait for nginx
sleep 5

echo -e "${YELLOW}Obtaining SSL certificate...${NC}"
docker compose run --rm certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    $DOMAIN_ARGS \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email

if [ $? -eq 0 ]; then
    echo -e "${GREEN}SSL certificate obtained successfully!${NC}"
    echo -e "${YELLOW}Restarting nginx with SSL configuration...${NC}"
    docker compose restart nginx
    echo -e "${GREEN}Done! Your site should now be accessible via HTTPS${NC}"
else
    echo -e "${RED}Failed to obtain SSL certificate${NC}"
    exit 1
fi
