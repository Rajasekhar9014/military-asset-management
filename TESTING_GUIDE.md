# 🧪 Complete Testing Guide - Step by Step

**Time Required:** 15-20 minutes  
**Current Status:** Both servers running ✅

---

## ✅ STEP 1: Check Servers Are Running

### Backend Server
Look at your terminal - you should see a terminal running with:
```
C:\Users\Harinathreddy\OneDrive\Desktop\F-API\.venv\Scripts\python.exe -m uvicorn...
```

✅ **If you see this, backend is running!**

### Frontend Server
Look for another terminal running:
```
npm create vite@latest frontend -- --template react
```

✅ **If you see this, frontend is running!**

---

## 🔧 STEP 2: Test Backend API (5 minutes)

### 2.1 Open Backend API Documentation
1. **Open your web browser** (Chrome, Edge, Firefox, etc.)
2. **Type this URL:** `http://127.0.0.1:8000/docs`
3. **Press Enter**

**What you should see:**
- A page titled "FastAPI - Swagger UI"
- A list of API endpoints organized by sections:
  - Authentication
  - Users
  - Asset Categories
  - Purchases
  - Transfers
  - Dashboard

✅ **If you see this page, your backend is working!**

---

### 2.2 Test Login Endpoint

1. **Find the section called "auth"**
2. **Click on** `POST /api/v1/auth/login` (it will expand)
3. **Click the "Try it out" button** (top right of the section)
4. **You'll see a text box with example JSON**
5. **Replace it with this:**
   ```json
   {
     "username": "admin",
     "password": "Admin123!"
   }
   ```
6. **Click the blue "Execute" button**

**What you should see:**
- Response Code: `200`
- Response Body with:
  - `access_token`: A long string (JWT token)
  - `token_type`: "bearer"
  - `user`: Object with username, email, role

✅ **If you see an access_token, login is working!**

---

### 2.3 Authorize with Token

1. **Copy the `access_token` value** (the long string, without quotes)
2. **Scroll to the top of the page**
3. **Click the green "Authorize" button** (top right)
4. **A popup will appear**
5. **In the "Value" field, type:** `Bearer ` (with a space after)
6. **Paste your token after "Bearer "**
   - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
7. **Click "Authorize"**
8. **Click "Close"**

✅ **You're now authenticated!**

---

### 2.4 Test Dashboard Endpoint

1. **Find the section called "dashboard"**
2. **Click on** `GET /api/v1/dashboard/metrics`
3. **Click "Try it out"**
4. **Click "Execute"** (don't fill any parameters)

**What you should see:**
- Response Code: `200`
- Response Body with metrics like:
  ```json
  {
    "opening_balance": 1000,
    "closing_balance": 1250,
    "net_movement": 250,
    "purchases": 300,
    "transfer_in": 50,
    "transfer_out": 100,
    "total_value": 5250000.00
  }
  ```

✅ **If you see metrics data, your backend is fully working!**

---

## 🎨 STEP 3: Test Frontend Application (10 minutes)

### 3.1 Open Frontend
1. **Open a NEW browser tab**
2. **Type this URL:** `http://localhost:5173`
3. **Press Enter**

**What you should see:**
- A login page with:
  - "Military Asset Management" title
  - Username field
  - Password field
  - "Sign In" button
  - Demo credentials shown: "admin / Admin123!"

✅ **If you see the login page, your frontend is running!**

---

### 3.2 Test Login

1. **In the Username field, type:** `admin`
2. **In the Password field, type:** `Admin123!`
3. **Click the "Sign In" button**

**What should happen:**
- Page redirects to `/dashboard`
- You see a navigation bar at top with:
  - "Military Asset Management" logo
  - Links: Dashboard, Purchases, Transfers
  - "Welcome, System Administrator"
  - Logout button

✅ **If you're redirected to dashboard, login works!**

---

### 3.3 Test Dashboard

**What you should see on the dashboard:**

1. **8 Colorful Metric Cards:**
   - Opening Balance (blue gradient)
   - Closing Balance (green gradient)
   - Net Movement (purple gradient)
   - Total Value (orange gradient)
   - Purchases (pink gradient)
   - Transfer In (teal gradient)
   - Transfer Out (red gradient)
   - Assigned (indigo gradient)

2. **Each card shows:**
   - A number (the metric value)
   - A label (the metric name)

3. **Filter Section at Top:**
   - Date Range (Start Date, End Date)
   - Unit dropdown
   - Category dropdown
   - "Apply Filters" button

✅ **If you see all 8 cards with numbers, dashboard is working!**

---

### 3.4 Test Net Movement Popup

1. **Find the "Net Movement" card** (purple gradient)
2. **Click anywhere on the card**

**What should happen:**
- A popup/modal appears
- Shows "Movement Details"
- Displays breakdown:
  - Purchases: (number)
  - Transfer In: (number)
  - Transfer Out: (number)
  - Net Movement: (number)
- Has an "X" or "Close" button

3. **Click "Close" or "X" to close the popup**

✅ **If popup shows and closes, this feature works!**

---

### 3.5 Test Purchases Page

1. **Click "Purchases" in the navigation bar**

**What you should see:**
- Page title: "Purchases"
- Filter section (Date, Unit, Category)
- "+ New Purchase" button (top right)
- A table with columns:
  - ID
  - Asset
  - Unit
  - Category
  - Quantity
  - Unit Price
  - Total Amount
  - Purchase Date
  - Vendor
  - Actions

2. **Click the "+ New Purchase" button**

**What should happen:**
- A modal/popup form appears with fields:
  - Asset ID
  - Unit ID
  - Category ID
  - Quantity
  - Unit Price
  - Purchase Date
  - Vendor
  - Invoice Number
  - Notes
- "Create Purchase" and "Cancel" buttons

3. **Fill in the form:**
   - Asset ID: `1`
   - Unit ID: `1`
   - Category ID: `1`
   - Quantity: `10`
   - Unit Price: `1000`
   - Purchase Date: Click and select today's date
   - Vendor: `Test Vendor`
   - Invoice Number: `INV-001`

4. **Click "Create Purchase"**

**What should happen:**
- Modal closes
- New purchase appears in the table
- You see your test purchase with the data you entered

✅ **If purchase is created and appears in list, this works!**

---

### 3.6 Test Transfers Page

1. **Click "Transfers" in the navigation bar**

**What you should see:**
- Page title: "Transfers"
- Filter section
- "+ New Transfer" button
- A table with columns:
  - ID
  - Asset
  - From Unit
  - To Unit
  - Quantity
  - Transfer Date
  - Status (with colored badges)
  - Actions

2. **Click the "+ New Transfer" button**

**What should happen:**
- A modal form appears with fields:
  - Asset ID
  - From Unit ID
  - To Unit ID
  - Quantity
  - Transfer Date
  - Reason
  - Notes

3. **Fill in the form:**
   - Asset ID: `1`
   - From Unit ID: `1`
   - To Unit ID: `2`
   - Quantity: `5`
   - Transfer Date: Select today's date
   - Reason: `Test Transfer`

4. **Click "Create Transfer"**

**What should happen:**
- Modal closes
- New transfer appears in the table
- Status badge shows "PENDING" in yellow/orange color

✅ **If transfer is created with PENDING status, this works!**

---

### 3.7 Test Filters

1. **On any page (Dashboard, Purchases, or Transfers)**
2. **Try the date filters:**
   - Click "Start Date" and select a date
   - Click "End Date" and select a later date
   - Click "Apply Filters"

**What should happen:**
- Data refreshes
- Only items within date range are shown

3. **Try unit/category filters:**
   - Select a unit from dropdown
   - Click "Apply Filters"

**What should happen:**
- Data filters by selected unit

✅ **If filters change the displayed data, they work!**

---

### 3.8 Test Logout

1. **Click the "Logout" button** (top right, next to your name)

**What should happen:**
- You're redirected to the login page
- You're logged out

2. **Try to go back to dashboard:**
   - Type `http://localhost:5173/dashboard` in address bar
   - Press Enter

**What should happen:**
- You're automatically redirected back to login
- (Because you're not authenticated)

✅ **If you can't access dashboard without login, security works!**

---

## 📊 Testing Checklist

Mark each item as you test it:

### Backend Tests
- [ ] Backend API docs load at http://127.0.0.1:8000/docs
- [ ] Login endpoint returns access token
- [ ] Can authorize with token
- [ ] Dashboard metrics endpoint returns data
- [ ] All 24 endpoints visible in Swagger UI

### Frontend Tests
- [ ] Frontend loads at http://localhost:5173
- [ ] Login page displays correctly
- [ ] Can login with admin/Admin123!
- [ ] Dashboard shows 8 metric cards
- [ ] Net Movement popup opens and closes
- [ ] Can navigate to Purchases page
- [ ] Can create a new purchase
- [ ] Purchase appears in the list
- [ ] Can navigate to Transfers page
- [ ] Can create a new transfer
- [ ] Transfer appears with PENDING status
- [ ] Date filters work
- [ ] Unit/Category filters work
- [ ] Can logout successfully
- [ ] Can't access protected pages when logged out

---

## ✅ Success Criteria

**Your application is ready for deployment if:**

✅ All backend tests pass  
✅ All frontend tests pass  
✅ You can login and see data  
✅ You can create purchases and transfers  
✅ Filters work correctly  
✅ Logout works  

---

## 🐛 Troubleshooting

### Backend not loading?
**Problem:** http://127.0.0.1:8000/docs doesn't load

**Solution:**
1. Check terminal - is backend server running?
2. Look for errors in terminal
3. If not running, restart:
   ```bash
   cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\backend
   .venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

### Frontend not loading?
**Problem:** http://localhost:5173 doesn't load

**Solution:**
1. Check terminal - is frontend server running?
2. Look for errors
3. If not running, restart:
   ```bash
   cd C:\Users\Harinathreddy\OneDrive\Desktop\F-API\frontend
   npm run dev
   ```

### Login fails?
**Problem:** Login returns error

**Solutions:**
1. Check backend is running
2. Verify database has admin user
3. Check browser console (F12) for errors
4. Verify credentials: admin / Admin123!

### No data in dashboard?
**Problem:** Dashboard shows zeros or no data

**Solutions:**
1. Database might be empty
2. Create some purchases/transfers manually
3. Check backend terminal for database errors

### Can't create purchases/transfers?
**Problem:** Form submission fails

**Solutions:**
1. Check browser console (F12) for errors
2. Verify backend is running
3. Check you're logged in (token not expired)
4. Verify all required fields are filled

---

## 🎯 What's Next?

**After successful testing:**

1. **Take screenshots** of:
   - Login page
   - Dashboard with metrics
   - Purchases page
   - Transfers page
   - Backend API docs

2. **Proceed to deployment:**
   - Deploy backend to Render
   - Deploy frontend to Vercel
   - See `render_deployment_guide.md` and `vercel_deployment_guide.md`

3. **Create deliverables:**
   - PDF documentation
   - Video walkthrough
   - Code archive

**See `ACTION_CHECKLIST.md` for the complete roadmap!**

---

**Good luck with testing!** 🚀

**If everything works, you're ready for deployment!** 🎉
