# HotelLens

A full-stack hotel search and ranking web application built with Django. HotelLens fetches real-time hotel data from the Booking.com API, ranks results using a custom scoring algorithm, and presents them through a dark-themed UI with photo carousels, detail pages, and direct booking links.

🌐 **Live Demo — [hotellens.up.railway.app](https://hotellens.up.railway.app)**

---

## Features

- **Real-time hotel search** — live data from Booking.com via RapidAPI
- **Custom ranking algorithm** — hotels scored on review score, star rating, essential amenities, and luxury amenities
- **Parallel API fetching** — fetches 5 pages of results simultaneously using `ThreadPoolExecutor`
- **Photo carousels** — swipeable image galleries on every hotel card
- **Hotel detail pages** — full photo gallery, room info, cancellation policy, amenities, map link, and booking summary
- **Price filters** — search by min/max price per night
- **Dark UI** — custom dark theme with gold accents built from scratch

---

## Tech Stack

- **Backend** — Python, Django
- **Frontend** — HTML, CSS, vanilla JavaScript (no frameworks)
- **API** — Booking.com API via RapidAPI
- **Concurrency** — `concurrent.futures.ThreadPoolExecutor`
- **Deployment** — Railway

---

## How It Works

### Search Flow
1. User submits city, dates, guests, and optional price filters
2. `get_dest_id()` resolves the city to a Booking.com destination ID
3. `get_hotels()` fetches 5 pages of results in parallel (~100 hotels)
4. `get_amenities()` fetches facility data for each hotel in parallel
5. `rank_hotels()` scores every hotel and sorts by score

### Ranking Algorithm
Each hotel starts with a base score:
- `review_score × 10`
- `property_class (stars) × 5`

Then amenities are evaluated:
- **Essential amenities** (e.g. AC, parking, restaurant): `+1` if present, `-2` if missing
- **Luxury amenities** (e.g. spa, pool, minibar): `+4` if present

Final score is normalized to a 0–10 scale.

### Detail Page
Clicking a hotel fetches full details including high-res room photos, room description, cancellation policy, coordinates, and real-time pricing for the selected dates.

---

## Project Structure

```
hotellens/
├── hotels/
│   ├── templates/
│   │   ├── index.html       # Search form
│   │   ├── search.html      # Results page with carousels
│   │   └── hotel.html       # Hotel detail page
│   ├── search.py            # API calls (dest lookup, hotels, amenities, details)
│   ├── ranker.py            # Scoring and ranking logic
│   ├── views.py             # Django views
│   └── urls.py              # URL routing
├── hotellens/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── .env                     # API key (not committed)
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/liveprosperdie/hotellens.git
cd hotellens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```
RAPIDAPI_KEY=your_rapidapi_key_here
```
Get your key by subscribing to the [Booking.com API on RapidAPI](https://rapidapi.com/DataCrawler/api/booking-com15).

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Start the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Deployment

This project is deployed on [Railway](https://railway.com). To deploy your own instance:

1. Push the project to GitHub (ensure `.env` is in `.gitignore`)
2. Create a new project on Railway and connect your repo
3. Add `RAPIDAPI_KEY` as an environment variable in the Railway dashboard
4. Railway auto-detects Django and deploys

---

## API Usage Note

This project uses the Booking.com API via RapidAPI which has monthly request limits on free plans. Each search makes approximately 15–20 API calls (5 pages + amenities). The live demo may be rate-limited.

---

## Author

Built by [Shrey Pathak](https://github.com/liveprosperdie)
