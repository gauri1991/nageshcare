#!/bin/bash
# =====================================================
# Domain and SSL Verification Script
# For: nageshcare.com
# =====================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DOMAIN="nageshcare.com"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Domain and SSL Status Check${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check HTTP response
check_url() {
    local url=$1
    local response=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 "$url" 2>/dev/null)

    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓ $url - HTTP $response OK${NC}"
        return 0
    elif [ "$response" = "301" ] || [ "$response" = "302" ]; then
        echo -e "${YELLOW}→ $url - HTTP $response (Redirect)${NC}"
        return 0
    elif [ "$response" = "000" ]; then
        echo -e "${RED}✗ $url - Connection failed${NC}"
        return 1
    else
        echo -e "${YELLOW}! $url - HTTP $response${NC}"
        return 1
    fi
}

# 1. Check DNS Resolution
echo -e "${YELLOW}1. DNS Resolution Check:${NC}"
dns_result=$(nslookup $DOMAIN 2>/dev/null | grep -A1 "Name:" | grep "Address:" | head -1 | awk '{print $2}')
if [ -n "$dns_result" ]; then
    echo -e "${GREEN}✓ $DOMAIN resolves to: $dns_result${NC}"
else
    echo -e "${RED}✗ DNS resolution failed for $DOMAIN${NC}"
fi

# Also check www subdomain
www_dns=$(nslookup www.$DOMAIN 2>/dev/null | grep -A1 "Name:" | grep "Address:" | head -1 | awk '{print $2}')
if [ -n "$www_dns" ]; then
    echo -e "${GREEN}✓ www.$DOMAIN resolves to: $www_dns${NC}"
else
    echo -e "${YELLOW}! www.$DOMAIN DNS resolution failed${NC}"
fi

echo ""

# 2. Check HTTP Connectivity
echo -e "${YELLOW}2. HTTP Connectivity:${NC}"
check_url "http://$DOMAIN"
check_url "http://www.$DOMAIN"

echo ""

# 3. Check HTTPS/SSL
echo -e "${YELLOW}3. HTTPS/SSL Status:${NC}"
check_url "https://$DOMAIN"
check_url "https://www.$DOMAIN"

echo ""

# 4. Check SSL Certificate Details
echo -e "${YELLOW}4. SSL Certificate Details:${NC}"
ssl_check=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)

if [ -n "$ssl_check" ]; then
    echo -e "${GREEN}✓ SSL Certificate found:${NC}"
    echo "$ssl_check" | while IFS= read -r line; do
        echo "  $line"
    done

    # Check if certificate is valid
    not_after=$(echo "$ssl_check" | grep "notAfter" | cut -d= -f2)
    if [ -n "$not_after" ]; then
        expires_timestamp=$(date -d "$not_after" +%s 2>/dev/null)
        current_timestamp=$(date +%s)

        if [ -n "$expires_timestamp" ] && [ "$expires_timestamp" -gt "$current_timestamp" ]; then
            days_left=$(( ($expires_timestamp - $current_timestamp) / 86400 ))
            echo -e "  ${GREEN}Certificate valid for $days_left more days${NC}"
        fi
    fi
else
    echo -e "${RED}✗ No SSL certificate found or unable to connect${NC}"
fi

echo ""

# 5. Check Static Files
echo -e "${YELLOW}5. Static Files Check:${NC}"
static_check=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 5 "https://$DOMAIN/static/admin/css/base.css" 2>/dev/null)
if [ "$static_check" = "200" ]; then
    echo -e "${GREEN}✓ Static files are being served correctly${NC}"
elif [ "$static_check" = "404" ]; then
    echo -e "${RED}✗ Static files not found (run collectstatic)${NC}"
else
    echo -e "${YELLOW}! Static files check returned: HTTP $static_check${NC}"
fi

echo ""

# 6. Check Application Status
echo -e "${YELLOW}6. Application Status:${NC}"
app_check=$(curl -s -L --max-time 10 "https://$DOMAIN" 2>/dev/null | grep -i "django\|welcome\|home" | head -1)
if [ -n "$app_check" ]; then
    echo -e "${GREEN}✓ Application appears to be running${NC}"
else
    echo -e "${YELLOW}! Could not verify application status${NC}"
fi

echo ""

# 7. Recommendations
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Recommendations:${NC}"
echo -e "${BLUE}========================================${NC}"

if [ "$static_check" != "200" ]; then
    echo "• Run: python manage.py collectstatic"
fi

# Check if SSL redirect should be enabled
http_check=$(curl -s -o /dev/null -w "%{http_code}" "http://$DOMAIN" 2>/dev/null)
https_check=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" 2>/dev/null)

if [ "$https_check" = "200" ] && [ "$http_check" != "301" ] && [ "$http_check" != "302" ]; then
    echo "• SSL is working but HTTP→HTTPS redirect is not enabled"
    echo "  Update .env: SECURE_SSL_REDIRECT=True"
    echo "  Ensure .htaccess has SSL redirect rules uncommented"
fi

if [ -z "$ssl_check" ]; then
    echo "• Install SSL certificate via cPanel"
    echo "• Use Let's Encrypt for free SSL certificate"
fi

echo ""
echo -e "${GREEN}Check complete!${NC}"