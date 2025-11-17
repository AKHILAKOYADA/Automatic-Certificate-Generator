# 🚀 Quick Deployment Steps

## Step 1: Install Vercel CLI (if not already installed)
```bash
npm i -g vercel
```
Or download from: https://vercel.com/download

## Step 2: Test Locally First
```bash
vercel dev
```
This will:
- Start local Vercel environment
- Simulate serverless execution
- Let you test before deploying

Visit: http://localhost:3000

## Step 3: Deploy to Vercel

### Option A: Deploy via CLI
```bash
# Login to Vercel (first time only)
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Option B: Deploy via GitHub
1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your repository
4. Vercel will auto-detect settings (already configured via vercel.json)

## Step 4: Set Environment Variables in Vercel Dashboard

Go to: Your Project → Settings → Environment Variables

Add these:
```
FLASK_SECRET_KEY=Lri4zLPZrIe_4-sl59EKfui22wVAqRbcfB0xwW_M6rY
```

**Optional** (for email functionality - more secure than hardcoding):
```
SMTP_EMAIL=kucet.official@gmail.com
SMTP_PASSWORD=cstx vuaq cizi ixha
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

## Step 5: Verify Deployment

1. Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
2. Test the certificate generator:
   - Enter password: `kuce&t`
   - Upload template and data file
   - Generate certificates
   - Download ZIP

## ✅ Checklist

- [ ] `vercel.json` exists
- [ ] `api/index.py` exists  
- [ ] `app.py` updated (accepted changes)
- [ ] Tested locally with `vercel dev`
- [ ] Deployed to Vercel
- [ ] Environment variables set in Vercel dashboard
- [ ] Tested production deployment

## 🐛 Troubleshooting

If you see errors:

1. **Check Function Logs:**
   - Vercel Dashboard → Your Project → Functions → Logs
   - Look for error messages

2. **Verify Files:**
   ```bash
   # Make sure these files exist
   ls vercel.json
   ls api/index.py
   ```

3. **Check Environment Variables:**
   - Dashboard → Settings → Environment Variables
   - Make sure `FLASK_SECRET_KEY` is set

4. **Local Test:**
   ```bash
   vercel dev
   # Test at http://localhost:3000
   ```

## 📚 Need More Help?

- See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed explanations
- See `FIX_SUMMARY.md` for quick reference
- Check Vercel docs: https://vercel.com/docs

