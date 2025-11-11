# Vercel Deployment Guide

## Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com

## Deployment Steps

### 1. Login to Vercel
```bash
vercel login
```

### 2. Deploy
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- Project name? **edu-performance-tracker** (or your choice)
- Directory? **./** (press Enter)
- Override settings? **N**

### 3. Set Environment Variables (Optional)
In Vercel Dashboard:
- Go to your project settings
- Navigate to Environment Variables
- Add:
  - `SECRET_KEY`: Generate a secure key
  - `DEBUG`: Set to `False` for production

### 4. Production Deployment
```bash
vercel --prod
```

## Important Notes

### Database
- SQLite doesn't work well on Vercel (serverless)
- For production, use PostgreSQL or MySQL
- Consider using:
  - Vercel Postgres
  - Supabase
  - PlanetScale
  - Railway

### Static Files
- Static files are collected during build
- Served from `/static/` path

### Media Files
- File uploads won't persist on Vercel
- Use cloud storage:
  - AWS S3
  - Cloudinary
  - Vercel Blob

## Alternative: Use Railway or Render
For a simpler deployment with persistent storage:
- Railway: https://railway.app
- Render: https://render.com

Both support Django with SQLite better than Vercel.

## Build Settings in Vercel Dashboard
If deploying via dashboard:
- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`
