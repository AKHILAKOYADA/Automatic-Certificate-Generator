# 🚀 How to Redeploy on Vercel

## Method 1: Redeploy via Vercel Dashboard (Easiest)

### Step 1: Set Environment Variables First
1. Go to **Vercel Dashboard** → Your Project
2. Click **Settings** → **Environment Variables**
3. Add or update:
   - **Name**: `FLASK_SECRET_KEY`
   - **Value**: `Lri4zLPZrIe_4-sl59EKfui22wVAqRbcfB0xwW_M6rY`
   - **Environments**: Select all (Production, Preview, Development)
4. Click **Save**

### Step 2: Trigger Redeploy
**Option A: Redeploy Latest**
1. Go to **Deployments** tab
2. Find the latest deployment
3. Click the **three dots (⋯)** menu
4. Select **Redeploy**

**Option B: Deploy from GitHub**
1. Go to **Deployments** tab
2. Click **Create Deployment** or **Redeploy**
3. Vercel will pull latest code from GitHub and redeploy

---

## Method 2: Redeploy via Vercel CLI

### Step 1: Install Vercel CLI (if not installed)
```bash
npm i -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Redeploy
```bash
# Preview deployment (for testing)
vercel

# Production deployment
vercel --prod
```

---

## Method 3: Redeploy via Git Push (Auto-Deploy)

If your Vercel project is connected to GitHub:

### Step 1: Make a small change (optional trigger)
```bash
# Make a small change to trigger deployment
# Or just push current code
git push
```

### Step 2: Vercel auto-deploys
- Vercel automatically detects the push
- Creates a new deployment
- Uses environment variables from dashboard

---

## Method 4: Force Redeploy After Environment Variable Changes

If you **just added/updated environment variables**:

1. **Go to Deployments tab**
2. **Find the latest deployment**
3. **Click the three dots (⋯) → Redeploy**
4. **Make sure "Use existing Build Cache" is UNCHECKED** (for fresh build)
5. **Click Redeploy**

This ensures the new environment variables are picked up.

---

## ✅ Verify Deployment Worked

### 1. Check Deployment Status
- Go to **Deployments** tab
- Look for ✅ **Ready** status (green)
- If ❌ **Error**, click to see logs

### 2. Test Your App
- Visit your Vercel URL
- Try the certificate generator
- Verify flash messages work (test wrong password)

### 3. Check Function Logs
- Go to **Functions** tab
- Click on a function (e.g., `api/index.py`)
- View **Logs** to see if errors occurred

---

## 🔍 Troubleshooting

### Issue: Changes Not Reflecting
**Solution:**
1. Clear browser cache
2. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
3. Check deployment logs for build errors

### Issue: Environment Variables Not Working
**Solution:**
1. Make sure you clicked **Save** after adding variables
2. **Redeploy** (environment variables only apply to new deployments)
3. Verify variable names match exactly (case-sensitive!)

### Issue: Build Fails
**Solution:**
1. Check **Build Logs** in deployment
2. Verify `requirements.txt` has all dependencies
3. Check `vercel.json` is valid JSON
4. Verify `api/index.py` exists

---

## 📋 Quick Checklist

Before redeploying:
- [ ] Environment variables set in Vercel dashboard
- [ ] All code changes committed and pushed to Git
- [ ] `vercel.json` is correct
- [ ] `api/index.py` exists
- [ ] `requirements.txt` has all dependencies

After redeploying:
- [ ] Deployment shows ✅ Ready status
- [ ] Tested app functionality
- [ ] Checked function logs for errors
- [ ] Verified environment variables are working

---

## 🎯 Most Common Scenario

**You just added `FLASK_SECRET_KEY` environment variable:**

1. ✅ Go to Dashboard → Settings → Environment Variables
2. ✅ Add `FLASK_SECRET_KEY` with your key
3. ✅ Click Save
4. ✅ Go to Deployments tab
5. ✅ Click three dots on latest deployment → **Redeploy**
6. ✅ Wait for deployment to complete
7. ✅ Test your app

---

## 💡 Pro Tips

- **Always redeploy after changing environment variables**
- **Check logs if deployment fails** - Vercel shows detailed errors
- **Use preview deployments** first to test before production
- **Keep deployment history** - you can revert to previous versions

