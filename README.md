# Traditional China Tours 🏯

A beautiful FastAPI-powered travel tour website for a 10-day journey through Beijing, Xi'an, and Shanghai.

## Features

- **Home** - Hero section, About Us, China Essentials, and Photo Gallery
- **Itinerary** - Detailed 10-day journey breakdown
- **Inclusions** - Comprehensive list of what's included
- **Reserve** - Booking form with form validation

## Tech Stack

- **Framework:** FastAPI
- **Templates:** Jinja2
- **Styling:** Custom CSS (Cormorant Garamond + DM Sans)
- **Server:** Uvicorn
- **Deployment:** Docker / systemd on VPS

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload

# Visit http://127.0.0.1:8000
```

## Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## VPS Deployment (Hostinger)

### 1. Clone to VPS

```bash
cd /var/www
sudo git clone <your-repo-url> traditionalchina
cd traditionalchina
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install systemd service

```bash
sudo cp fastapi.service /etc/systemd/system/traditionalchina.service
sudo systemctl daemon-reload
sudo systemctl enable --now traditionalchina
```

### 3. Configure Nginx

```nginx
server {
    server_name traditionalchina.travel www.traditionalchina.travel;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/traditionalchina/static;
        expires 30d;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/traditionalchina /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL with Certbot

```bash
sudo certbot --nginx -d traditionalchina.travel -d www.traditionalchina.travel
```

## Project Structure

```
traditionalchina/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image config
├── docker-compose.yaml # Docker compose config
├── fastapi.service     # systemd service file
├── templates/
│   ├── base.html       # Base template with nav/footer
│   ├── home.html       # Home page
│   ├── itinerary.html  # Itinerary page
│   ├── inclusions.html # Inclusions page
│   └── reserve.html    # Reservation form
└── static/
    ├── css/
    │   └── style.css   # Main stylesheet
    └── images/         # Tour images
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/itinerary` | GET | 10-day itinerary |
| `/inclusions` | GET | What's included |
| `/reserve` | GET | Reservation form |
| `/api/reserve` | POST | Submit reservation |
| `/subscribe` | POST | Newsletter signup |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |

## Customization

### Images
Replace placeholder Unsplash URLs in `templates/home.html` with your own tour photos.

### Contact Info
Update email and phone in `templates/base.html` footer.

### Departure Dates
Edit the `<select>` options in `templates/reserve.html`.

---

Built with ❤️ using FastAPI
