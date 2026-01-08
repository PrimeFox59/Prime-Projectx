# Prime Projectx

Modern landing page and proposal management system for engineering & system development services. Built with Flask and Firebase Firestore.

## 🌟 Features
- **Multi-language support**: Indonesian (ID), English (EN), and Japanese (JP)
- **Dark neon-themed UI**: Futuristic design with live particle animation and video background
- **Client inquiry system**: Public form for project inquiries
- **Admin dashboard**: Full CRUD for proposals, highlights, and inquiries
- **Proposal sharing**: QR codes + secure tokenized links for client access
- **Firebase Firestore**: Scalable NoSQL database with real-time capabilities
- **AI-focused messaging**: Marketing copy emphasizes AI/ML integration
- **Contact integration**: WhatsApp, LinkedIn, and email links

## 🚀 Tech Stack
- **Backend**: Flask 3.x (Python)
- **Database**: Firebase Firestore (NoSQL)
- **Frontend**: Vanilla JavaScript, CSS3 (Grid/Flexbox)
- **Deployment**: Vercel-ready with `vercel.json`
- **Features**: QR code generation, session management, multi-language

## 📦 Installation

### Prerequisites
- Python 3.11+
- Firebase project with Firestore enabled
- Firebase service account credentials JSON

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/prime-projectx.git
   cd prime-projectx
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Firebase setup**
   - Create Firebase project at [console.firebase.google.com](https://console.firebase.google.com/)
   - Enable Firestore Database
   - Download service account JSON
   - Save as `firebase-credentials.json` in project root
   - See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions

5. **Environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

6. **Run the app**
   ```bash
   python app.py
   ```
   Open http://127.0.0.1:5050

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
```

### Firestore Collections
- `quotes` - Proposal/quotation documents
- `inquiries` - Client inquiry submissions
- `highlights` - Service capability cards on landing page

## 📱 Admin Access
1. Click the **gear icon** in top-right corner
2. Login with admin credentials (default: `admin` / `admin123`)
3. Manage proposals, highlights, and view inquiries

## 🌍 Multi-Language Support
- **ID** (Indonesian) - Default, Bahasa Indonesia
- **EN** (English) - International English  
- **JP** (Japanese) - 日本語

Language switcher in navigation bar. Selection persists in session.

## 🚀 Deployment to Vercel

### Quick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/prime-projectx)

### Manual Deployment
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set environment variables:
     - `SECRET_KEY`
     - `ADMIN_USERNAME`
     - `ADMIN_PASSWORD`
     - `GOOGLE_APPLICATION_CREDENTIALS` (paste firebase-credentials.json content)

3. **Deploy**
   - Vercel will auto-deploy from `main` branch
   - See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed deployment guide

## 📂 Project Structure
```
prime-projectx/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── firebase-credentials.json  # Firebase service account (gitignored)
├── .gitignore
├── templates/            # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── quotation.html
│   ├── admin_base.html
│   ├── admin_dashboard.html
│   ├── admin_quote_form.html
│   └── admin_highlight_form.html
└── static/               # Static assets
    ├── css/main.css
    ├── js/main.js
    ├── video/bg.mp4
    └── icon.png
```

## 📖 Documentation
- [FIREBASE_SETUP.md](FIREBASE_SETUP.md) - Detailed Firebase setup and deployment guide
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Development guidelines

## 🔒 Security Notes
- **Never commit** `firebase-credentials.json` to version control
- Change default admin credentials in production
- Use strong `SECRET_KEY` in production
- Review Firestore security rules before going live

## 📞 Contact Information
- **WhatsApp**: +6289524257778
- **LinkedIn**: [linkedin.com/in/galihprime](https://www.linkedin.com/in/galihprime/)
- **Email**: primetroyxs@gmail.com

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing
This is a portfolio/client project. For inquiries or collaboration, please contact via the methods above.

## 🎯 Roadmap
- [ ] Real-time collaboration features
- [ ] Email notifications for new inquiries
- [ ] PDF export for proposals
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support

## 🙏 Acknowledgments
Built for PT Pakarti Riken Indonesia and manufacturing industry clients.
- QR codes are generated on the fly at `/qr/<token>`.
