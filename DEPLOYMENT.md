# VoltShield Compliance - Deployment Guide

## Quick Start - Deploy to Render.com (FREE)

### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize access to your repositories

### Step 2: Create a New Web Service
1. Click "New +" → "Web Service"
2. Select your `Voltshield` repository
3. Fill in these settings:
   - **Name**: voltshield-api (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Step 3: Add Environment Variables
Before deploying, add these environment variables in Render:
- `SENDER_EMAIL`: Your Gmail address (e.g., your-email@gmail.com)
- `SENDER_PASSWORD`: Your Gmail App Password (see below)
- `BUSINESS_EMAIL`: Your business email to receive notifications
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587

### Step 4: Get Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication if not already enabled
3. Go to "App passwords" (search for it)
4. Select "Mail" and "Windows Computer" (or your device)
5. Copy the 16-character password
6. Use this as `SENDER_PASSWORD` in Render

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 2-3 minutes for deployment
3. You'll get a URL like: `https://voltshield-api.onrender.com`

### Step 6: Update Your HTML
In your `index.html`, find this line (around line 515):
```javascript
const BACKEND_URL = "https://your-backend-url.com";
```

Replace it with:
```javascript
const BACKEND_URL = "https://voltshield-api.onrender.com";
```

### Step 7: Enable GitHub Pages
1. Go to your repository Settings
2. Scroll to "GitHub Pages"
3. Select "Deploy from a branch"
4. Choose `main` branch, `/ (root)` folder
5. Save

Your website will be live at: `https://amdiallo1.github.io/voltshield/`

---

## Testing Your Setup

1. Visit your GitHub Pages website
2. Scroll down and fill out the booking form
3. Click "Submit Booking"
4. You should receive:
   - A confirmation email at the customer's email
   - A notification email at your business email

---

## Alternative Deployment Options

### Railway.app (Also Free)
1. Go to https://railway.app
2. Click "New Project"
3. Deploy from GitHub
4. Select your repository
5. Add environment variables
6. Done!

### Heroku (Paid - $5+/month)
1. Go to https://www.heroku.com
2. Click "Create New App"
3. Connect to GitHub
4. Enable auto-deploy from main branch
5. Add environment variables in Settings
6. Done!

---

## Troubleshooting

### Form submissions not working?
- Check that `BACKEND_URL` in HTML matches your deployed backend URL
- Check browser console (F12) for error messages
- Verify environment variables are set in Render

### Not receiving emails?
- Check spam/promotions folder
- Verify `SENDER_EMAIL` and `SENDER_PASSWORD` are correct
- Ensure Gmail App Password is used (not regular password)
- Check Render logs for errors

### Backend not starting?
- Go to Render dashboard
- Click on your service
- Check "Logs" tab for errors
- Ensure all dependencies in `requirements.txt` are correct

---

## Next Steps

1. **Automate deployments**: Every time you push to `main`, Render will auto-deploy
2. **Add database**: Store bookings in a real database (PostgreSQL)
3. **Add admin dashboard**: View and manage bookings
4. **Integrate with calendars**: Sync with Google Calendar or Outlook
5. **Add payment processing**: Accept payments through Stripe

---

**Need Help?**
- Render Support: https://render.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- GitHub Pages Help: https://docs.github.com/en/pages
