#!/bin/bash
# Traditional China Tours - VPS Deployment Script
# Run this on your Hostinger VPS after cloning the repository

set -e

echo "🏯 Traditional China Tours - Deployment Script"
echo "=============================================="

# Configuration
APP_DIR="/var/www/traditionalchina"
DOMAIN="traditionalchina.travel"
SERVICE_NAME="traditionalchina"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "📦 Installing system dependencies..."
apt update
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git

echo "📂 Setting up application directory..."
mkdir -p $APP_DIR
cd $APP_DIR

echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn[standard] jinja2 aiofiles python-multipart

echo "📋 Creating systemd service..."
cat > /etc/systemd/system/${SERVICE_NAME}.service << 'EOF'
[Unit]
Description=Traditional China Tours - FastAPI
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/traditionalchina
Environment="PATH=/var/www/traditionalchina/venv/bin"
ExecStart=/var/www/traditionalchina/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "🔧 Configuring Nginx..."
cat > /etc/nginx/sites-available/${DOMAIN} << EOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    location /static {
        alias /var/www/traditionalchina/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "✅ Testing Nginx configuration..."
nginx -t

echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}
systemctl restart nginx

echo "🔒 Setting up SSL with Let's Encrypt..."
certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos --email admin@${DOMAIN} || echo "SSL setup requires manual verification"

echo ""
echo "✨ Deployment Complete!"
echo "======================"
echo "Your site should now be live at: https://${DOMAIN}"
echo ""
echo "Useful commands:"
echo "  - View logs:     sudo journalctl -u ${SERVICE_NAME} -f"
echo "  - Restart app:   sudo systemctl restart ${SERVICE_NAME}"
echo "  - Restart nginx: sudo systemctl restart nginx"

