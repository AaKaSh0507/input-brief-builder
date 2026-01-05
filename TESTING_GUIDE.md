# 🧪 COMPLETE TESTING GUIDE

## ✅ **All Issues Fixed**

1. ✅ HTTPS Mixed Content - Fixed
2. ✅ Excel file selection (.xlsx) - Fixed  
3. ✅ Undefined brief ID error - Fixed
4. ✅ Backend schema updated (6 sections) - Done
5. ✅ Excel extraction working - Tested

---

## 🚀 **Step-by-Step Testing Instructions**

### **Step 1: Clear Browser Cache**

**IMPORTANT:** Do a hard refresh to clear cached files:
- **Windows/Linux**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`
- Or clear browser cache in settings

### **Step 2: Open Browser Console**

Press `F12` to open Developer Tools and check:
- ✅ Should see: "Backend URL configured as: https://..."
- ✅ Should see: "GPJ Input Brief Assistant initialized"
- ❌ Should NOT see: Mixed Content errors
- ❌ Should NOT see: 404 errors for undefined

---

## 📝 **Test Workflow**

### **Test 1: Create New Brief**

1. **Click "New Brief" button** on Dashboard
   
2. **Enter Title** (when prompted):
   ```
   Customer Contact Week 2025
   ```

3. **Enter Event Type** (when prompted):
   ```
   3rd Party
   ```

4. **Expected Result:**
   - ✅ Brief created successfully
   - ✅ Redirects to Brief Editor
   - ✅ Shows 6 sections in sidebar:
     1. Project Overview
     2. Project Stakeholders
     3. Objectives & Audience
     4. Story & Client Experience
     5. Historical Learnings
     6. Agency Deliverables

5. **Check Console:**
   - ✅ No errors
   - ✅ See successful POST to `/api/briefs/`

---

### **Test 2: Upload Excel File**

1. **In Brief Editor**, scroll to **"Uploaded Documents"** section

2. **Click "Choose File"** button

3. **Select your Excel file**:
   ```
   2025 Events GPJ View filtered for AI Input Brief v1.xlsx
   ```

4. **Expected Result:**
   - ✅ File uploads automatically
   - ✅ Shows in document list with filename
   - ✅ Shows upload date
   - ✅ Shows delete button (🗑️)

5. **Check Console:**
   - ✅ See successful POST to `/api/documents/upload`
   - ✅ Response includes `extracted_content` with your data

---

### **Test 3: Auto-Populate Section**

1. **Navigate to "Project Overview"** section

2. **Click "Auto-populate from docs"** button

3. **Wait for AI processing** (5-10 seconds)

4. **Expected Result:**
   - ✅ Shows "Processing..." or loading state
   - ✅ Fields get populated with data from Excel:
     - Project Name: "Customer Contact Week 2025"
     - EMB: "UACBLCMB"
     - Event Date: "2025-06-09"
     - City: "Las Vegas"
     - Country: "USA"
     - Budget: "$145,000"
     - etc.

5. **Check Console:**
   - ✅ See POST to `/api/ai/auto-populate/{section_id}`
   - ✅ Response includes structured data

6. **Check "AI Suggestions" box** (should appear at bottom)
   - ✅ Shows extracted data in blue box

---

### **Test 4: Manual Field Entry**

1. **In any section**, try adding/editing data manually

2. **Add custom field**:
   - Click "Add Custom Field"
   - Enter field name (e.g., "Special Requirements")
   - Enter value

3. **Navigate to Next Section**
   - Click "Next Section →" button

4. **Expected Result:**
   - ✅ Data is auto-saved
   - ✅ Can navigate back and see saved data

---

### **Test 5: Review Multiple Sections**

1. **Navigate through all 6 sections** using sidebar

2. **For each section, try:**
   - Viewing current content
   - Auto-populating from Excel
   - Manually editing fields

3. **Expected Sections:**

   **1. Project Overview**
   - Basic Details (15 fields)
   - Sponsorship Components

   **2. Project Stakeholders**
   - Client Information (7 contacts)
   - GPJ Information (3 contacts)

   **3. Objectives & Audience**
   - Primary Objectives
   - Client Journey
   - Outcomes & Targets
   - Previous Year Results
   - Target Audience
   - Relationship
   - Industry Context

   **4. Story & Client Experience**
   - Client Experience
   - Key Message & Value Proposition
   - Use Cases
   - Client Stories
   - Feature Products & Demos
   - Integration
   - Other Considerations

   **5. Historical Learnings**
   - Previous Year Results
   - Historical Learnings
   - Meeting Space
   - Efficiency Gains

   **6. Agency Deliverables**
   - Event Must Haves
   - Pre-designed Floor Plan
   - Blue Studio Deliverables

---

### **Test 6: Export to PDF**

1. **Click "Export PDF"** button (top right)

2. **Expected Result:**
   - ✅ PDF file downloads
   - ✅ Filename: `brief_{id}.pdf`
   - ✅ Opens in PDF viewer

3. **Check PDF Content:**
   - ✅ Has title page
   - ✅ Shows all 6 sections
   - ✅ Shows populated fields
   - ✅ Professional formatting

---

### **Test 7: Return to Dashboard**

1. **Click "← Back to Dashboard"**

2. **Expected Result:**
   - ✅ Returns to Dashboard
   - ✅ Shows your created brief in list
   - ✅ Shows status badge (DRAFT)
   - ✅ Shows metadata (date, version)

---

## 🐛 **If You Encounter Errors:**

### **Error: "Failed to upload document"**

**Check:**
1. Is the brief saved? (Should not be "new")
2. Is file size < 100MB?
3. Is file format .xlsx or .xls?
4. Check console for specific error

**Solution:**
- Make sure brief is created first
- Try a smaller file
- Check file format

---

### **Error: "Failed to create brief"**

**Check:**
1. Is backend running? (Check `/api/health`)
2. Is PostgreSQL running?
3. Any errors in browser console?

**Solution:**
- Run startup script: `/app/scripts/startup.sh`
- Check backend logs: `tail -50 /var/log/supervisor/backend.err.log`

---

### **Error: "Section not found"**

**Check:**
1. Were sections created automatically?
2. Check API response for brief creation

**Solution:**
- Delete brief and create new one
- Sections should auto-create

---

### **Error: Mixed Content (HTTP/HTTPS)**

**Should be fixed, but if it persists:**

**Check:**
1. Browser console shows: "Backend URL configured as: https://..."
2. All API requests use HTTPS

**Solution:**
- Hard refresh browser (Ctrl+Shift+R)
- Clear cache completely
- Check `window.location.origin` in console

---

## ✅ **Success Checklist**

After testing, you should be able to:

- [x] Create new brief with title
- [x] See 6 sections in sidebar
- [x] Upload Excel file (.xlsx)
- [x] View uploaded document in list
- [x] Auto-populate sections from Excel
- [x] See AI-extracted data in fields
- [x] Manually edit fields
- [x] Navigate between sections
- [x] Save progress automatically
- [x] Export brief to PDF
- [x] Return to dashboard
- [x] See brief in list

---

## 📊 **Your Excel File Data**

**Events in your file:**
1. Customer Contact Week 2025 (UACBLCMB)
2. Gartner IT Conference (ARLR9LMB)
3. VMware Explore 2025 (64ZICGMB)
4. MaximoWorld 2025 (GDDQJHMB)
5. And 7 more...

**Fields extracted:**
- Event Name, EMB #
- Start/End Dates
- Location (City, State)
- Event Website
- Producer
- Execution Cost
- Event Tier
- Stakeholder Names

**Test with:** Customer Contact Week 2025
- Most complete data
- Good for testing all fields

---

## 🎯 **Expected AI Extraction Results**

When you auto-populate "Project Overview" with your Excel:

```json
{
  "Project Name": "Customer Contact Week 2025",
  "EMB": "UACBLCMB",
  "Event Date": "2025-06-09",
  "Venue": "Will extract from data",
  "City": "Las Vegas",
  "Country": "USA",
  "Producer": "customer management practice",
  "Forecasted Budget": "$145,000",
  "Event Tier": "2",
  "Website": "customercontactweekdigital.com"
}
```

---

## 🔧 **Quick Commands**

**Restart All Services:**
```bash
/app/scripts/startup.sh
```

**Check Backend Health:**
```bash
curl https://basic-spec-builder.preview.emergentagent.com/api/health
```

**Check Frontend:**
```bash
curl https://basic-spec-builder.preview.emergentagent.com/
```

**View Logs:**
```bash
# Backend
tail -50 /var/log/supervisor/backend.err.log

# Frontend
tail -50 /var/log/supervisor/frontend.err.log
```

---

## 📞 **Support**

If issues persist after testing:

1. Check browser console for errors
2. Check service logs
3. Run startup script
4. Clear browser cache
5. Try incognito/private window

---

**Ready for thorough testing! Follow the steps above and let me know what works and what doesn't.** 🚀
