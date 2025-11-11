# Vercel Deployment Guide

## IMPORTANT: Database Setup Required

Your app is currently failing because SQLite doesn't work on Vercel. You MUST set up a PostgreSQL database first.

## Quick Fix: Set Up Database

### Option 1: Vercel Postgres (Recommended)
1. Go to your Vercel project dashboard
2. Click on **Storage** tab
3. Click **Create Database**
4. Select **Postgres**
5. Follow the setup wizard
6. Vercel will automatically add `DATABASE_URL` to your environment variables

### Option 2: Supabase (Free)
1. Go to https://supabase.com
2. Create a new project
3. Get your database connection string from Project Settings > Database
4. Format: `postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres`

### Option 3: Railway (Free)
1. Go to https://railway.app
2. Create a new project
3. Add PostgreSQL service
4. Copy the `DATABASE_URL` from the service

## Add Environment Variables to Vercel

1. Go to your Vercel project dashboard
2. Click **Settings** > **Environment Variables**
3. Add these variables:

```
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=your-secret-key-here-generate-a-long-random-string
DEBUG=False
```

4. Click **Save**
5. Redeploy your project

## Redeploy

After adding the database URL:

```bash
vercel --prod
```

Or trigger a redeploy from the Vercel dashboard.

## Run Migrations

After first deployment with database:
1. Go to Vercel Dashboard > Deployments
2. Click on your latest deployment
3. Go to Functions tab
4. You may need to run migrations manually or add to build script

## Alternative: Deploy to Railway Instead

Railway is easier for Django apps:

1. Go to https://railway.app
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Connect your repository
5. Railway will:
   - Automatically detect Django
   - Provide PostgreSQL database
   - Set up environment variables
   - Handle migrations

Railway is recommended for Django apps with databases!

## Build Settings in Vercel Dashboard

- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

## Media Files Note

File uploads still won't persist on Vercel. For production:
- Use AWS S3
- Use Cloudinary
- Use Vercel Blob Storage
