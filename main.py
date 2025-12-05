"""
Traditional China Tours - FastAPI Application
A beautiful travel tour website powered by FastAPI
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Traditional China Tours",
    description="10-day journey through Beijing, Xi'an, and Shanghai",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with hero, about, essentials, and gallery sections"""
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "active_page": "home"}
    )


@app.get("/itinerary", response_class=HTMLResponse)
async def itinerary(request: Request):
    """10-day itinerary page"""
    return templates.TemplateResponse(
        "itinerary.html",
        {"request": request, "active_page": "itinerary"}
    )


@app.get("/inclusions", response_class=HTMLResponse)
async def inclusions(request: Request):
    """What's included page"""
    return templates.TemplateResponse(
        "inclusions.html",
        {"request": request, "active_page": "inclusions"}
    )


@app.get("/reserve", response_class=HTMLResponse)
async def reserve(request: Request):
    """Reservation form page"""
    return templates.TemplateResponse(
        "reserve.html",
        {"request": request, "active_page": "reserve"}
    )


@app.post("/api/reserve")
async def submit_reservation(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    travelers: str = Form(...),
    departure: str = Form(...),
    room_type: str = Form(None),
    dietary: str = Form(None),
    message: str = Form(None),
    how_heard: str = Form(None)
):
    """Handle reservation form submissions"""
    # In production, you would:
    # - Save to database
    # - Send confirmation email
    # - Notify admin
    reservation = {
        "name": f"{first_name} {last_name}",
        "email": email,
        "phone": phone,
        "travelers": travelers,
        "departure": departure,
        "room_type": room_type,
        "dietary": dietary,
        "message": message,
        "how_heard": how_heard,
        "submitted_at": datetime.utcnow().isoformat()
    }
    print(f"New reservation: {reservation}")
    
    # Redirect to a thank you response or page
    return templates.TemplateResponse(
        "reserve.html",
        {
            "request": request,
            "active_page": "reserve",
            "success": True,
            "message": f"Thank you, {first_name}! We've received your reservation request and will contact you within 24 hours."
        }
    )


@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    """Handle newsletter subscriptions"""
    print(f"Newsletter subscription: {email}")
    # In production, add to mailing list (Mailchimp, SendGrid, etc.)
    return RedirectResponse(url="/?subscribed=true", status_code=303)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Traditional China Tours",
        "version": "1.0.0"
    }


@app.get("/api/info")
async def api_info(request: Request):
    """API information endpoint"""
    return {
        "app": "Traditional China Tours",
        "version": "1.0.0",
        "python": "3.11+",
        "framework": "FastAPI",
        "server": "Uvicorn",
        "host": str(request.base_url),
        "pages": {
            "home": "/",
            "itinerary": "/itinerary",
            "inclusions": "/inclusions",
            "reserve": "/reserve"
        },
        "api_endpoints": {
            "docs": "/docs",
            "health": "/health",
            "reserve": "/api/reserve",
            "subscribe": "/subscribe"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
