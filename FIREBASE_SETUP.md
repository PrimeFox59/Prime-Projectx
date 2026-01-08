# Prime Projectx - Firestore Setup Guide

## Firebase Configuration

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project" or select existing project
3. Enable Firestore Database:
   - Go to "Firestore Database" in left menu
   - Click "Create Database"
   - Choose "Start in production mode" or "Test mode"
   - Select location (asia-southeast2 recommended for Indonesia)

### 2. Get Service Account Credentials

#### For Local Development:
1. In Firebase Console, go to Project Settings (gear icon) > Service Accounts
2. Click "Generate New Private Key"
3. Download the JSON file
4. Rename it to `firebase-credentials.json`
5. Place it in project root (same folder as app.py)
6. **IMPORTANT**: Add `firebase-credentials.json` to `.gitignore` (already added)

#### For Production (Vercel):
1. Use the same JSON file from above
2. In Vercel dashboard:
   - Go to your project > Settings > Environment Variables
   - Create variable: `GOOGLE_APPLICATION_CREDENTIALS`
   - Paste the ENTIRE contents of firebase-credentials.json as value
   - OR upload as file (if Vercel supports it)

### 3. Firestore Collections Structure

The app uses 3 collections:

#### `quotes` collection:
```
{
  token: string (unique)
  client_name: string
  project_name: string
  scope: string
  amount: number
  status: string (Draft/Proposal/Approved)
  technical_approach: string
  deliverables: string
  timeline: string
  tech_stack: string
  team_structure: string
  assumptions: string
  payment_terms: string
  created_at: timestamp
}
```

#### `inquiries` collection:
```
{
  client_name: string
  project_name: string
  scope: string
  contact: string
  budget: number (optional)
  status: string
  created_at: timestamp
}
```

#### `highlights` collection:
```
{
  category: string
  title: string
  body: string
  display_order: number
  created_at: timestamp
}
```

### 4. Firestore Security Rules (Production)

Go to Firestore > Rules tab and paste:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read access for quotes and highlights
    match /quotes/{quoteId} {
      allow read: if true;
      allow write: if false; // Only backend can write
    }
    
    match /highlights/{highlightId} {
      allow read: if true;
      allow write: if false; // Only backend can write
    }
    
    // Inquiries - allow create from public, read from backend only
    match /inquiries/{inquiryId} {
      allow create: if true; // Allow public to submit
      allow read, update, delete: if false; // Only backend
    }
  }
}
```

### 5. Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure firebase-credentials.json is in project root
# Run the app
python app.py
```

### 6. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

#### Option B: GitHub + Vercel Auto-Deploy
1. Push code to GitHub
2. Import project in Vercel dashboard
3. Set environment variables:
   - `SECRET_KEY`: your-secret-key
   - `ADMIN_USERNAME`: admin
   - `ADMIN_PASSWORD`: your-password
   - `GOOGLE_APPLICATION_CREDENTIALS`: paste firebase-credentials.json content

#### Create `vercel.json` for deployment:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 7. Seed Sample Data (Optional)

After deployment, you can add sample data via Firebase Console or create a seed script:

```python
# seed_data.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add sample quote
db.collection('quotes').add({
    'token': 'sample-token-123',
    'client_name': 'PT Example Company',
    'project_name': 'Sample Project',
    'scope': 'Web application development',
    'amount': 5000000,
    'status': 'Draft',
    'created_at': firestore.SERVER_TIMESTAMP
})

print("Sample data added!")
```

### Troubleshooting

**Error: "Could not automatically determine credentials"**
- Make sure `firebase-credentials.json` exists in project root
- OR set GOOGLE_APPLICATION_CREDENTIALS environment variable

**Error: "Permission Denied"**
- Check Firestore Security Rules
- Make sure service account has proper permissions

**Vercel Deployment Issues:**
- Verify environment variables are set correctly
- Check Vercel logs for detailed error messages
- Ensure firebase-credentials.json content is valid JSON

## Architecture Benefits

✅ **Scalability**: Firestore scales automatically  
✅ **Real-time**: Can add real-time features later  
✅ **Serverless**: No database server to manage  
✅ **Global CDN**: Low latency worldwide  
✅ **Free Tier**: Generous free quota for small projects

## Migration from SQLite

Your existing SQLite data is backed up in `app.py.sqlite.bak`. To migrate:
1. Export data from SQLite manually
2. Import to Firestore via Firebase Console or seed script
3. Or start fresh (old data is preserved in backup)
