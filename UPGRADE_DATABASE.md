# 🔄 Database Upgrade Instructions

Database model telah di-upgrade dengan field baru untuk proposal yang lebih lengkap!

## Field Baru yang Ditambahkan:

### 📋 Proposal Details
- `technical_approach` - Pendekatan teknis & metodologi
- `deliverables` - List deliverables yang akan diserahkan
- `timeline` - Timeline/schedule proyek
- `tech_stack` - Technology stack yang digunakan
- `team_structure` - Struktur tim yang terlibat
- `assumptions` - Assumptions & dependencies
- `payment_terms` - Terms of payment

## Cara Upgrade Database:

### Option 1: Delete & Recreate (Recommended untuk Development)
```powershell
# Stop aplikasi (Ctrl+C di terminal)
# Delete database lama
Remove-Item prime_projectx.db

# Run aplikasi lagi - database akan dibuat otomatis
python app.py
```

### Option 2: Manual Migration (Untuk Production dengan Data Penting)
```powershell
# Backup dulu
Copy-Item prime_projectx.db prime_projectx_backup.db

# Akses SQLite shell
sqlite3 prime_projectx.db

# Add kolom baru satu per satu
ALTER TABLE quotation ADD COLUMN technical_approach TEXT;
ALTER TABLE quotation ADD COLUMN deliverables TEXT;
ALTER TABLE quotation ADD COLUMN timeline TEXT;
ALTER TABLE quotation ADD COLUMN tech_stack TEXT;
ALTER TABLE quotation ADD COLUMN team_structure TEXT;
ALTER TABLE quotation ADD COLUMN assumptions TEXT;
ALTER TABLE quotation ADD COLUMN payment_terms TEXT;

# Exit
.exit
```

## Setelah Upgrade:

1. ✅ Login ke `/admin`
2. ✅ Klik "Add New" di section Quotations
3. ✅ Lihat form baru dengan section:
   - 📋 Informasi Dasar
   - 🔧 Rencana Teknis
   - 📅 Timeline & Resources
   - 📝 Terms & Conditions
4. ✅ Isi field sesuai kebutuhan (hanya 4 field wajib: Client, Project, Scope, Amount)
5. ✅ Save → System auto-generate token + QR code
6. ✅ Share link atau QR ke client
7. ✅ Client akses proposal lengkap dengan semua detail!

## 🎯 Cara Membuat Proposal ke Client:

### Step 1: Admin Login
1. Buka browser → http://127.0.0.1:5050/admin
2. Login dengan:
   - Username: `admin`
   - Password: `admin123`

### Step 2: Create New Proposal
1. Klik tombol **"Add New"** di bagian Recent Proposals
2. Isi form proposal:

#### Informasi Dasar (Wajib):
- **Client/Company**: Nama perusahaan client
- **Nama Proyek**: Judul proyek
- **Scope of Work**: Deskripsi umum scope
- **Investment Amount**: Nilai investasi dalam Rupiah
- **Status**: Draft/Proposal/Approved/In Progress/Completed

#### Rencana Teknis (Opsional tapi Recommended):
- **Technical Approach**: 
  ```
  Contoh:
  - Menggunakan Agile methodology dengan 2-week sprints
  - Microservices architecture untuk scalability
  - RESTful API design dengan JWT authentication
  ```

- **Technology Stack**:
  ```
  Contoh:
  Frontend: React.js, TailwindCSS
  Backend: Flask/Python, PostgreSQL
  DevOps: Docker, GitHub Actions
  Cloud: AWS EC2, RDS, S3
  ```

- **Deliverables**:
  ```
  Contoh:
  - Web application dengan responsive design
  - Admin dashboard dengan role management
  - REST API documentation (Swagger)
  - Database design & migration scripts
  - User manual & training materials
  - 3 months post-launch support
  ```

#### Timeline & Resources:
- **Project Timeline**:
  ```
  Contoh:
  Phase 1 (Week 1-2): Requirements gathering & UI/UX design
  Phase 2 (Week 3-6): Core development & API integration
  Phase 3 (Week 7-8): Testing & bug fixing
  Phase 4 (Week 9): UAT & deployment
  Phase 5 (Week 10-12): Stabilization & training
  ```

- **Team Structure**:
  ```
  Contoh:
  1x Project Manager (Full-time)
  2x Full-stack Developer (Full-time)
  1x UI/UX Designer (Part-time)
  1x QA Engineer (Part-time)
  1x DevOps Engineer (On-demand)
  ```

#### Terms & Conditions:
- **Assumptions & Dependencies**:
  ```
  Contoh:
  - Client menyediakan akses ke production server & database
  - Existing API documentation tersedia
  - UAT akan diselesaikan dalam 2 minggu
  - Scope freeze setelah design approval
  ```

- **Payment Terms**:
  ```
  Contoh:
  30% - Down payment (setelah kontrak signed)
  40% - Development milestone (setelah UAT passed)
  30% - Go-live (setelah deployment success)
  
  Payment via transfer bank dalam 14 hari invoice
  ```

### Step 3: Save Proposal
1. Klik tombol **"💾 Save Proposal"**
2. System akan:
   - ✅ Generate unique token (misal: `aBc123XyZ`)
   - ✅ Create QR code otomatis
   - ✅ Generate shareable link
3. Flash message muncul: "Proposal berhasil disimpan! Link & QR code siap di-share."

### Step 4: Share ke Client

#### Cara 1: Copy Link
1. Buka proposal yang baru dibuat
2. Klik tombol **"Copy Link"**
3. Share via:
   - Email
   - WhatsApp
   - Slack
   - Atau platform komunikasi lainnya

#### Cara 2: Download QR Code
1. Right-click pada QR code image
2. "Save image as..."
3. Kirim QR code via:
   - Email attachment
   - Print di proposal document
   - Tampilkan di presentasi
   - Share di chat

#### Cara 3: Direct Access
Link format: `http://127.0.0.1:5050/q/[TOKEN]`

Contoh: `http://127.0.0.1:5050/q/aBc123XyZ`

### Step 5: Client Access Proposal

Client membuka link atau scan QR → Melihat proposal lengkap dengan:

✅ Project overview & scope
✅ Technical approach & methodology
✅ Technology stack details
✅ Deliverables checklist
✅ Project timeline & milestones
✅ Team structure
✅ Assumptions & dependencies
✅ Payment terms & schedule
✅ Investment amount dengan format Rupiah
✅ Status badge (Draft/Proposal/Approved)

## 📱 Fitur untuk Client:

- ✅ Bisa akses 24/7 dari device manapun (desktop/tablet/mobile)
- ✅ No login required - secure via unique token
- ✅ Professional dark theme interface
- ✅ Copy link untuk share internal
- ✅ Download QR code
- ✅ Responsive design - mobile friendly

## 🔒 Security:

- Token generated dengan `secrets.token_urlsafe()` - cryptographically strong
- 64 character unique identifier
- Tidak bisa di-guess atau brute force
- Database indexed untuk fast lookup

## 💡 Tips:

1. **Status Workflow**:
   - `Draft` → Internal review
   - `Proposal` → Sent to client
   - `Approved` → Client approved
   - `In Progress` → Development ongoing
   - `Completed` → Project delivered

2. **Update Proposal**:
   - Admin bisa edit proposal kapan saja
   - Link & QR tetap sama (token tidak berubah)
   - Client otomatis lihat versi terbaru

3. **Multiple Proposals**:
   - Bisa create unlimited proposals
   - Setiap proposal punya token unik sendiri
   - Track via admin dashboard

4. **Template Reuse**:
   - Copy-paste dari proposal sebelumnya yang sukses
   - Standardize deliverables & terms
   - Maintain consistency

## 🎉 Ready!

Sekarang Anda bisa membuat proposal profesional dengan mudah dan share ke client via QR code atau link!
