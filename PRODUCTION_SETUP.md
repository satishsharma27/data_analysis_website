# Data Analytics Website - Production Setup

## Overview

Your website has been successfully merged with the marketing dashboard. The application now includes:

- **Main Website**: Flask-based website with portfolio, services, and contact form at `/`
- **Interactive Dashboard**: Dash-based marketing analytics dashboard at `/dashboard/` 
- **Production Ready**: Debug mode disabled, proper error handling, and WSGI-ready

## Project Structure

```
.
├── app.py                      # Flask entrypoint for deployment
├── dashboard_app/              # Application package
│   ├── __init__.py             # App factory and dashboard registration
│   ├── dashboard.py            # Dash dashboard layout and callbacks
│   ├── data.py                 # Marketing CSV loading and KPI calculations
│   ├── routes.py               # Main website routes and error handlers
│   └── utils.py                # Shared formatting and color constants
├── Marketing.csv               # Sample marketing data (replace with your data)
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html              # Main website template
│   ├── automation-section.html
│   ├── data-analysis.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── style.css               # Website styles
│   └── dashboard-style.css     # Dashboard styles
└── venv/                       # Virtual environment
```

## Installation & Setup

### 1. Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Prepare Your Data

Replace `Marketing.csv` with your actual data. Required columns:
- `c_date` - Date (YYYY-MM-DD format)
- `impressions` - Number of impressions
- `clicks` - Number of clicks
- `leads` - Number of leads
- `revenue` - Revenue amount
- `mark_spent` - Marketing spend
- `orders` - Number of orders
- `category` - Campaign category (social, search, influencer, media)
- `campaign_name` - Campaign name

### 3. Run Locally (Development)

```bash
python app.py
```

The application will run on `http://localhost:5001`

- Main website: `http://localhost:5001/`
- Dashboard: `http://localhost:5001/dashboard/`

## Production Deployment

### Option 1: Using Gunicorn (Recommended)

```bash
gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:5001 --timeout 120 app:server
```

### Option 2: Using uWSGI

```bash
pip install uwsgi

uwsgi --http :5001 --wsgi-file app.py --callable server --processes 4 --threads 2
```

### Option 3: Using Waitress

```bash
pip install waitress

waitress-serve --port=5001 app:server
```

## Nginx Configuration (Optional)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /dashboard {
        proxy_pass http://127.0.0.1:5001/dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Key Features

✅ **Integrated Dashboard**: Marketing analytics directly in your website  
✅ **Production Ready**: Debug mode disabled, proper error handling  
✅ **Responsive Design**: Works on desktop, tablet, and mobile  
✅ **Interactive Charts**: Plotly-powered visualizations  
✅ **Category Filtering**: Filter dashboard data by campaign category  

## Dashboard Metrics

The dashboard displays:

- **Total Impressions** - With CTR percentage
- **Total Clicks** - With conversion rate
- **Total Revenue** - With ROAS (Return on Ad Spend)
- **Marketing Spend** - With ACOS (Advertising Cost of Sale)
- **Revenue Trend** - Line chart over time
- **Clicks by Category** - Donut chart breakdown
- **Top Campaigns** - Horizontal bar chart
- **Category Comparison** - Grouped bar chart

## Customization

### Update Colors

Edit `/app.py` and modify the color variables in the dashboard setup section:

```python
BLUE   = "#378ADD"
TEAL   = "#1D9E75"
AMBER  = "#BA7517"
# ... etc
```

### Modify KPI Cards

Add or remove KPI cards by editing the `app.layout` in `/app.py`:

```python
kpi_card("Label", "Value", "Delta", is_up)
```

### Change Dashboard Data

Ensure your `Marketing.csv` has the required columns and run the app.

## Troubleshooting

### Port Already in Use

```bash
lsof -i :5001
kill -9 <PID>
```

### Module Not Found

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Dashboard Not Loading

Check that `Marketing.csv` exists in the project root and has the correct format.

## Environment Variables (Optional)

Create a `.env` file for configuration:

```
FLASK_ENV=production
DASH_DEBUG=false
```

## Support

For issues or customizations, ensure:
1. All dependencies are installed
2. `Marketing.csv` has correct columns and format
3. Port 5001 is not in use
4. File permissions are correct

---

**Last Updated**: April 2026  
**Version**: 1.0  
**Status**: Production Ready
