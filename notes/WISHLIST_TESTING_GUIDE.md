# 🧪 Wishlist Feature - Complete Testing & Troubleshooting Guide

## ✅ Pre-Testing Setup

### Step 1: Verify Django Installation
```bash
# Make sure you're in the project directory
cd c:\Users\Asus\django_project\LEARNING

# Activate virtual environment (if using one)
# Windows:
env1\Scripts\activate

# Linux/Mac:
source env1/bin/activate
```

### Step 2: Check Database
```bash
# Run migrations (if needed)
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser
```

### Step 3: Start Development Server
```bash
python manage.py runserver

# Should see:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

### Step 4: Open Browser
```
Go to: http://127.0.0.1:8000
Browser: Chrome, Firefox, Safari, or Edge (modern versions)
```

---

## 🧪 Test Suite 1: Basic Functionality

### Test 1.1: Login
**Objective**: Ensure user can login

**Steps**:
1. Go to http://127.0.0.1:8000/login/
2. Enter your test username
3. Enter your test password
4. Click "Login" button

**Expected Result**:
- ✓ Redirected to home page
- ✓ Username displayed in navbar
- ✓ User is authenticated

**If Failed**:
- Check username/password are correct
- Verify user exists in database
- Check database connection

---

### Test 1.2: Navigate to Food Detail Page
**Objective**: Verify food detail page loads correctly

**Steps**:
1. Go to http://127.0.0.1:8000/foods/allfoods
2. Click on any food item
3. Should see food details page

**Expected Result**:
- ✓ Food image displayed
- ✓ Food title, price, rating shown
- ✓ Three action buttons visible: [Add to Cart] [Customize] [♡ Save]
- ✓ Heart icon button is visible

**If Failed**:
- Check if fooddetails.html was updated
- Verify food item has valid image
- Check browser console for errors

---

### Test 1.3: Heart Icon Button is Present
**Objective**: Confirm heart icon button renders

**Steps**:
1. On food detail page, look for action buttons
2. Count the buttons: should be 3
3. Third button should show heart icon (♡ or ♥)

**Expected Result**:
- ✓ Three buttons visible
- ✓ Third button shows "♡ Save" (outline heart + text)
- ✓ Button is clickable

**If Failed**:
```
Troubleshooting:
1. Check Bootstrap Icons are loaded in base.html
   Look for: <link rel="stylesheet" href="...icons.css">
   
2. Check if <i class="bi bi-heart"></i> renders
   Open F12 → Elements → Find the button
   
3. Check CSS is applied
   Open F12 → Styles → Look for .btn-wishlist styling
```

---

## 🧪 Test Suite 2: Add to Wishlist

### Test 2.1: Click Heart Icon (Not Logged In)
**Objective**: Verify login requirement

**Steps**:
1. Logout if logged in
2. Go to any food detail page
3. Click the heart icon (♡ Save)

**Expected Result**:
- ✓ Alert appears: "Please log in first to save items to your wishlist."
- ✓ Redirected to login page after clicking OK

**If Failed**:
```
Troubleshooting:
Check browser console (F12 → Console):
- Look for JavaScript errors
- Should see: "alertLoginRequired()" called
```

---

### Test 2.2: Click Heart Icon (Logged In)
**Objective**: Add item to wishlist with AJAX

**Steps**:
1. Login first
2. Go to any food detail page
3. Click the heart icon (♡ Save)
4. **Important**: Do NOT refresh the page

**Expected Result (Immediate)**:
- ✓ Heart icon fills with red (♥)
- ✓ Text changes from "Save" to "Saved"
- ✓ Button background becomes light red (#fff0f0)
- ✓ Button border becomes red
- ✓ Toast notification appears: "Food Name added to wishlist!"
- ✓ Page does NOT reload
- ✓ Other buttons remain unchanged

**Visual Feedback**:
```
Before:  [♡ Save]     (gray outline, white bg)
         ↓ (click)
After:   [♥ Saved]    (red fill, light red bg, red border)
         
Toast appears (top-right):
┌─────────────────────────┐
│ ✓ Pizza added to        │
│   wishlist!             │
└─────────────────────────┘
```

**If Not Working**:
```
Check:
1. Browser Console (F12):
   - Look for Network errors
   - Look for JavaScript errors
   - Should see 200 OK response to /foods/wishlist/toggle/ID/
   
2. Network Tab:
   - Click Heart
   - Should see GET request to /foods/wishlist/toggle/ID/
   - Response should be JSON: {"added": true, "food_name": "...", ...}
   
3. Database:
   - Check if Wishlist record was created
   - python manage.py shell
   - from foods.models import Wishlist
   - Wishlist.objects.all()  # Should show your entry
```

---

### Test 2.3: Add Same Item Again (Duplicate Prevention)
**Objective**: Verify duplicates are prevented

**Steps**:
1. Don't reload page
2. Click the same heart icon again (now filled red)
3. It should toggle OFF

**Expected Result**:
- ✓ Heart becomes outline again (♡)
- ✓ Text changes back to "Save"
- ✓ Background becomes white
- ✓ Toast notification: "Pizza removed from wishlist."
- ✓ Can add again and it works

**If Failed**:
```
Troubleshooting:
1. Check database constraint:
   - Look for error: "duplicate key value"
   
2. Verify unique_together in Wishlist model:
   - Should have: unique_together = ('user', 'food')
   
3. If model changed, run:
   - python manage.py makemigrations
   - python manage.py migrate
```

---

## 🧪 Test Suite 3: Wishlist Page

### Test 3.1: Navigate to Wishlist
**Objective**: Access wishlist page

**Steps**:
1. Add 3-5 items to wishlist
2. Click "Wishlist" in navbar
   (Or go to: http://127.0.0.1:8000/foods/wishlist/)

**Expected Result**:
- ✓ Beautiful gradient header appears
- ✓ Shows count: "5 food items saved"
- ✓ Products displayed in grid
- ✓ Grid adapts to screen size

**If Not Showing**:
```
Troubleshooting:
1. Check URL works:
   - Go directly to /foods/wishlist/
   - If 404, check urls.py has the route
   
2. Check items are in database:
   - python manage.py shell
   - from foods.models import Wishlist
   - from django.contrib.auth.models import User
   - user = User.objects.first()
   - Wishlist.objects.filter(user=user).count()
   
3. Check template renders:
   - Verify wishlist.html exists
   - Check for template errors in console
```

---

### Test 3.2: Check Card Display
**Objective**: Verify wishlist cards show correctly

**Steps**:
1. View wishlist page
2. Look at any card
3. Should show: Image, Category, Name, Description, Price

**Expected Result** (Professional Card):
```
┌──────────────────┐
│  🍕 Food Image   │
├──────────────────┤
│ PIZZA            │
│ Pizza Name       │
│ Description...   │
│ ₹299             │
├──────────────────┤
│[Move to Cart][♥] │
└──────────────────┘
```

**If Incorrect**:
```
Troubleshooting:
1. Image not showing:
   - Check food has food_img
   - Verify media files directory exists
   
2. Price not showing:
   - Check food.price exists
   - Verify fooditem queryset in view
   
3. Styling off:
   - Hard refresh: Ctrl+Shift+R
   - Clear browser cache
   - Check CSS file loaded
```

---

### Test 3.3: Responsive Layout
**Objective**: Verify grid layout adapts to screen sizes

**Steps**:
1. View wishlist on desktop (browser window max width)
2. Should see 4 columns of cards
3. Resize browser to tablet size (~768px)
4. Should see 3 columns
5. Resize to mobile (~480px)
6. Should see 1-2 columns

**Expected Result**:
- ✓ Layout adapts smoothly
- ✓ No overflow or broken layout
- ✓ All text readable at any size
- ✓ Buttons clickable on mobile

**If Not Responsive**:
```
Troubleshooting:
1. Check CSS media queries in wishlist.html
   - Should have @media (max-width: 768px)
   - Should have @media (max-width: 480px)
   
2. Test in browser DevTools:
   - F12 → Device Toggle (Ctrl+Shift+M)
   - Select different devices
   - Check layout changes
   
3. Check Grid CSS:
   - row-cols-1, row-cols-sm-2, row-cols-md-3, row-cols-xl-4
```

---

### Test 3.4: Move to Cart Button
**Objective**: Verify "Move to Cart" button works

**Steps**:
1. On wishlist page
2. Click "🛒 Move to Cart" on any card
3. Page should redirect to cart

**Expected Result**:
- ✓ Item appears in shopping cart
- ✓ Item removed from wishlist
- ✓ Success message shown
- ✓ Count on wishlist decreases

**If Failed**:
```
Troubleshooting:
1. Check wishlist_to_cart view exists
   - Look in views.py
   
2. Check Cart model:
   - Verify Cart.objects.get_or_create works
   
3. Check item was created:
   - Go to cart page
   - Item should be there
```

---

### Test 3.5: Remove from Wishlist (Heart Icon)
**Objective**: Remove item from wishlist page

**Steps**:
1. On wishlist page
2. Click heart icon (♥) on any card
3. Should remove immediately

**Expected Result**:
- ✓ Card disappears (or reloads list)
- ✓ Count decreases
- ✓ Toast notification appears
- ✓ Can be added back

**If Failed**:
```
Troubleshooting:
Check if toggle_wishlist is being called:
1. F12 → Network → Click heart
2. Should see request to /foods/wishlist/toggle/ID/
3. Check response is valid JSON
```

---

## 🧪 Test Suite 4: Edge Cases

### Test 4.1: Empty Wishlist
**Objective**: Test empty state

**Steps**:
1. Remove all items from wishlist
2. Go to wishlist page

**Expected Result**:
- ✓ Beautiful empty state displayed
- ✓ Message: "No saved items yet"
- ✓ "Browse Foods" button visible and clickable
- ✓ Clicking button goes to allfoods page

**If Failed**:
```
Check:
1. Empty state HTML in wishlist.html
2. CSS for .empty-wish class
3. Button link: {% url 'allfoods' %}
```

---

### Test 4.2: Multiple Users
**Objective**: Test data isolation between users

**Steps**:
1. User A: Add items to wishlist
2. Note items in User A's wishlist
3. Logout
4. Login as User B
5. Go to wishlist
6. Should be empty (different user)

**Expected Result**:
- ✓ User B's wishlist is empty
- ✓ User A's items don't appear
- ✓ Data properly isolated

**If Failed**:
```
Troubleshooting:
1. Check Wishlist model filters by user:
   - Wishlist.objects.filter(user=request.user)
   
2. Verify login_required decorator:
   - All wishlist views should have @login_required
```

---

### Test 4.3: Browser Back Button
**Objective**: Test browser navigation

**Steps**:
1. Add item to wishlist
2. Go to wishlist page
3. Click "Browse Foods"
4. Use browser back button
5. Should see updated wishlist

**Expected Result**:
- ✓ Navigation works smoothly
- ✓ Data persists correctly
- ✓ No errors on back navigation

---

## 🛠️ Troubleshooting Guide

### Issue: Heart Icon Not Showing

**Symptom**: Button shows just text "[Save]" without heart icon

**Solutions**:
```
1. Check Bootstrap Icons in base.html
   Location: templates/base.html
   Look for: <link href="...bootstrap-icons.css">
   
   If missing, add:
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

2. Check if <i> tag is rendering
   F12 → Inspect element → Check for <i class="bi bi-heart">

3. Clear cache:
   Ctrl+Shift+Delete → Clear browser cache
   Then: Ctrl+Shift+R to hard refresh
```

---

### Issue: AJAX Not Working (Page Reloads)

**Symptom**: Page reloads instead of smooth AJAX update

**Solutions**:
```
1. Check JavaScript is enabled:
   F12 → Console → Should not show JS errors
   
2. Check X-Requested-With header:
   F12 → Network → Click heart → Check request headers
   Should show: X-Requested-With: XMLHttpRequest
   
3. Check server response:
   F12 → Network → Click heart → Check response
   Should be valid JSON:
   {"added": true, "food_name": "...", ...}
   
4. Check for JavaScript errors:
   F12 → Console → Look for red errors
   Common: "toggleWishlist is not defined"
   Solution: Verify script section in fooddetails.html
```

---

### Issue: Items Not Saving to Database

**Symptom**: Can click heart, but items don't appear in wishlist page

**Solutions**:
```
1. Check user is authenticated:
   - Verify logged-in username in navbar
   - @login_required should prevent unauthenticated access
   
2. Check database:
   python manage.py shell
   >>> from foods.models import Wishlist
   >>> from django.contrib.auth.models import User
   >>> user = User.objects.get(username='testuser')
   >>> Wishlist.objects.filter(user=user).count()
   
   Should show > 0 if items are saved
   
3. Check migrations:
   python manage.py migrate
   
4. Check database connection:
   python manage.py dbshell
   SELECT * FROM foods_wishlist;
   Should show records
```

---

### Issue: Styling Not Applied

**Symptom**: Colors, spacing, or effects not showing

**Solutions**:
```
1. Hard refresh page:
   Windows: Ctrl+Shift+R
   Mac: Cmd+Shift+R
   
2. Clear browser cache:
   Settings → Clear browsing data → CSS/Cache
   
3. Check CSS is in HTML:
   F12 → Inspect → Look for <style> section
   Check if .btn-wishlist and .w-card styles present
   
4. Check for CSS conflicts:
   F12 → Elements → Right-click element
   Select "Inspect" → Check Styles tab
   Look for crossed-out CSS (conflicts)
   
5. Check CSS validity:
   Look for syntax errors in style section
   Each rule should be: selector { property: value; }
```

---

### Issue: Button Not Clickable

**Symptom**: Heart icon button exists but doesn't respond

**Solutions**:
```
1. Check onclick handler:
   Inspect element → Should have:
   onclick="toggleWishlist(FOOD_ID)"
   
2. Check JavaScript function exists:
   F12 → Console → type: toggleWishlist
   Should show: ƒ toggleWishlist(foodId)
   
3. Check for JavaScript errors:
   F12 → Console → Look for errors
   
4. Check if logged in:
   If not logged in, should show alert
   
5. Check URL in fetch request:
   Should be: /foods/wishlist/toggle/FOOD_ID/
   Verify this URL is in urls.py
```

---

### Issue: Data Not Visible in Wishlist Page

**Symptom**: Wishlist page loads but shows empty even with saved items

**Solutions**:
```
1. Check database has items:
   python manage.py shell
   >>> from foods.models import Wishlist
   >>> from django.contrib.auth.models import User
   >>> user = User.objects.first()
   >>> Wishlist.objects.filter(user=user)
   
2. Check queryset in view:
   foods/views.py, wishlist_view():
   items = Wishlist.objects.filter(user=request.user)
   
3. Check template context:
   Should have: 'items': items
   
4. Check template rendering:
   {% if items %}
   Should be looping through items
   {% for item in items %}
   
5. Check related food objects load:
   May need: .select_related('food')
   to avoid N+1 queries
```

---

## 📊 Performance Testing

### Test: Page Load Time
```
1. Open Developer Tools (F12)
2. Go to Network tab
3. Reload page
4. Should see:
   - Total load time: < 2 seconds
   - Wishlist API: < 200ms
```

### Test: No N+1 Queries
```
1. Go to Django shell:
   python manage.py shell
   
2. Enable query logging:
   from django.test.utils import override_settings
   
3. Query wishlist:
   from foods.models import Wishlist
   items = Wishlist.objects.filter(user=user).select_related('food')
   
4. Should see: 2 queries (Wishlist + Food join)
   Not: 1 + N queries (Wishlist + 1 per food)
```

---

## ✅ Final Verification Checklist

Before considering the feature complete:

- [ ] Heart icon button displays on food detail page
- [ ] Icon fills with red when clicked (saved state)
- [ ] Text changes from "Save" to "Saved"
- [ ] AJAX works (no page reload)
- [ ] Toast notification appears
- [ ] Wishlist page shows saved items
- [ ] Professional styling applied
- [ ] Responsive on mobile
- [ ] Empty state displays correctly
- [ ] Move to Cart button works
- [ ] Remove button works
- [ ] Login requirement enforced
- [ ] Duplicate prevention works
- [ ] Multiple users can have separate wishlists
- [ ] Database stores items correctly
- [ ] No JavaScript console errors
- [ ] No CSS issues or conflicts
- [ ] All animations smooth
- [ ] Buttons clickable on all devices

---

## 📞 Getting Help

If issues persist:

1. **Check Documentation**:
   - WISHLIST_IMPLEMENTATION_COMPLETE.md
   - WISHLIST_QUICK_REFERENCE.md
   - WISHLIST_VISUAL_DESIGN_GUIDE.md

2. **Check Server Logs**:
   - Look at Django console output
   - Check for 500/400 errors

3. **Check Browser Console**:
   - F12 → Console tab
   - Look for red error messages

4. **Check Database**:
   - `python manage.py shell`
   - Query Wishlist records directly

5. **Verify Files Were Updated**:
   - Check file modification times
   - Verify code matches the guide

---

**Good luck with testing! 🎉**
