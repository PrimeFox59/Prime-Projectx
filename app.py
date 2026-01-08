import os
import secrets
import io
import json
import textwrap
from datetime import datetime, timezone, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, session
import qrcode
import firebase_admin
from firebase_admin import credentials, firestore
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Initialize Firebase
if not firebase_admin._apps:
    # Try to get credentials from environment variable first (for Vercel)
    cred_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    if cred_json:
        # Environment variable contains JSON string
        try:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except json.JSONDecodeError:
            # If JSON parsing fails, try as file path
            if os.path.exists(cred_json):
                cred = credentials.Certificate(cred_json)
                firebase_admin.initialize_app(cred)
            else:
                raise ValueError("Invalid GOOGLE_APPLICATION_CREDENTIALS")
    elif os.path.exists('firebase-credentials.json'):
        # Local development - use file
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("Firebase credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS environment variable or add firebase-credentials.json")

db = firestore.client()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Contact Information
CONTACT_WHATSAPP = "+6289524257778"
CONTACT_LINKEDIN = "https://www.linkedin.com/in/galihprime/"
CONTACT_EMAIL = "primetroyxs@gmail.com"
CONTACT_FASTWORK = "https://fastwork.id/user/glh_prima"

TRANSLATIONS = {
    "id": {
        "nav_services": "Layanan",
        "nav_workflow": "Alur Kerja",
        "nav_quotes": "Penawaran",
        "nav_admin": "Admin",
        "hero_eyebrow": "Engineering & System Development Solutions",
        "hero_title": "Prime Projectx",
        "hero_desc": "Membangun sistem cerdas berbasis AI untuk mengakselerasi produktivitas manufaktur Anda. Mulai dari digitalisasi alur kerja, kontrol kualitas statistik, hingga platform manajemen terintegrasi dengan AI analytics—dirancang presisi untuk kebutuhan industri modern.",
        "hero_btn_primary": "Konsultasi Gratis",
        "hero_btn_secondary": "Eksplorasi Portofolio",
        "hero_metric_1": "sistem aktif",
        "hero_metric_2": "mitra industri",
        "hero_metric_3": "uptime support",
        "capabilities_title": "Keahlian Kami",
        "capabilities_desc": "Solusi end-to-end untuk transformasi digital manufaktur dengan integrasi AI—dari otomasi dokumen, machine learning untuk quality control, hingga analitik prediktif yang mendorong efisiensi operasional dan decision-making berbasis data.",
        "workflow_title": "Proses Kolaborasi",
        "workflow_step_1": "Requirement Gathering",
        "workflow_step_1_desc": "Diskusi mendalam untuk memahami tantangan bisnis, mapping kebutuhan stakeholder, dan validasi kelayakan teknis.",
        "workflow_step_2": "System Design",
        "workflow_step_2_desc": "Merancang arsitektur yang scalable, desain database optimal, wireframe intuitif, serta strategi integrasi dengan sistem eksisting.",
        "workflow_step_3": "Development Sprint",
        "workflow_step_3_desc": "Implementasi bertahap dengan AI-assisted coding, automated testing, dokumentasi real-time, dan review berkala bersama tim Anda. Memanfaatkan AI tools untuk code optimization dan quality assurance.",
        "workflow_step_4": "Quality Assurance",
        "workflow_step_4_desc": "User acceptance testing bersama end-user, stress testing performa, security hardening, dan compliance verification.",
        "workflow_step_5": "Go-Live & Support",
        "workflow_step_5_desc": "Deployment terencana, training komprehensif untuk user, knowledge transfer, serta maintenance dan enhancement berkelanjutan.",
        "workflow_box_title": "Track Record Terpercaya",
        "workflow_box_subtitle": "Solusi nyata untuk hasil terukur",
        "workflow_box_bullet_1": "6+ sistem production-ready di PT Pakarti Riken Indonesia",
        "workflow_box_bullet_2": "Spesialisasi di manufacturing execution & quality management systems",
        "workflow_box_bullet_3": "Full-stack expertise: Web apps, workflow automation, data analytics",
        "workflow_box_bullet_4": "Kaizen-driven approach untuk continuous improvement",
        "workflow_box_btn": "Mulai Diskusi Proyek",
        "inquiry_title": "Sampaikan Kebutuhan Anda",
        "inquiry_desc": "Ceritakan tantangan bisnis Anda, tim kami akan menyusun proposal komprehensif dengan scope detail, arsitektur solusi, dan estimasi investasi yang transparan.",
        "inquiry_client": "Nama Perusahaan",
        "inquiry_project": "Judul Proyek",
        "inquiry_scope": "Deskripsi Kebutuhan",
        "inquiry_scope_placeholder": "Contoh: Sistem tracking produksi real-time untuk 3 line assembly, integrasi dengan SAP, dashboard analytics",
        "inquiry_budget": "Estimasi Budget (Rp)",
        "inquiry_contact": "Email / WhatsApp",
        "inquiry_submit": "Ajukan Proposal",
        "inquiry_box_title": "Proses Transparan & Profesional",
        "inquiry_box_desc": "Setelah menerima inquiry, tim kami akan melakukan analisis mendalam dan menyusun proposal terstruktur dalam format digital yang mudah diakses.",
        "inquiry_box_bullet_1": "Proposal dikirim via secure link dengan QR code untuk kemudahan akses",
        "inquiry_box_bullet_2": "Dapat dibuka di semua device—desktop, tablet, atau smartphone",
        "inquiry_box_bullet_3": "Interface modern dengan visualisasi scope dan breakdown biaya yang jelas",
        "quotes_title": "Portofolio Proyek",
        "quotes_desc": "Sistem yang telah kami kembangkan untuk berbagai kebutuhan industri manufaktur.",
        "quote_view": "Detail",
        "footer_desc": "Engineering excellence untuk transformasi digital industri Anda.",
        "footer_capabilities": "Layanan",
        "footer_process": "Metodologi",
        "footer_quotations": "Portofolio",
        "footer_contact": "Hubungi Kami",
        "footer_meta": "Trusted partner untuk inovasi sistem manufaktur.",
        "quote_page_title": "Proposal Detail",
        "quote_label_client": "Client",
        "quote_label_project": "Project",
        "quote_label_scope": "Scope of Work",
        "quote_label_amount": "Investment",
        "quote_label_status": "Status",
        "quote_label_created": "Tanggal",
        "quote_copy_link": "Copy Link",
        "quote_invoice_btn": "Generate Invoice PDF",
        "quote_schedule_btn": "Schedule Meeting",
        "quote_qr_title": "Scan untuk membuka proposal",
        "admin_dashboard_title": "Admin Dashboard",
        "admin_highlights_title": "Service Highlights",
        "admin_inquiries_title": "Recent Inquiries",
        "admin_quotes_title": "Recent Proposals",
        "admin_logout": "Logout",
        "admin_add_new": "Add New",
        "admin_edit": "Edit",
        "admin_delete": "Delete",
    },
    "en": {
        "nav_services": "Services",
        "nav_workflow": "Workflow",
        "nav_quotes": "Quotes",
        "nav_admin": "Admin",
        "hero_eyebrow": "Engineering & System Development Solutions",
        "hero_title": "Prime Projectx",
        "hero_desc": "Accelerating manufacturing productivity through AI-powered intelligent system integration. From workflow digitization and statistical quality control to comprehensive management platforms with AI analytics—precision-engineered for modern industrial demands.",
        "hero_btn_primary": "Schedule Consultation",
        "hero_btn_secondary": "Explore Portfolio",
        "hero_metric_1": "active systems",
        "hero_metric_2": "industry partners",
        "hero_metric_3": "support uptime",
        "capabilities_title": "Our Expertise",
        "capabilities_desc": "End-to-end solutions for manufacturing digital transformation with AI integration—from document automation, machine learning for quality control, to predictive analytics that drive operational efficiency and data-driven decision-making.",
        "workflow_title": "Collaborative Process",
        "workflow_step_1": "Discovery & Analysis",
        "workflow_step_1_desc": "In-depth discussions to understand business challenges, stakeholder requirement mapping, and technical feasibility validation.",
        "workflow_step_2": "Solution Design",
        "workflow_step_2_desc": "Scalable architecture design, optimized database modeling, intuitive wireframes, and integration strategy with existing systems.",
        "workflow_step_3": "Agile Development",
        "workflow_step_3_desc": "Iterative implementation with AI-assisted coding, automated testing, real-time documentation, and regular reviews with your team. Leveraging AI tools for code optimization and quality assurance.",
        "workflow_step_4": "Quality Assurance",
        "workflow_step_4_desc": "User acceptance testing with end-users, performance stress testing, security hardening, and compliance verification.",
        "workflow_step_5": "Deployment & Enablement",
        "workflow_step_5_desc": "Planned rollout strategy, comprehensive user training, knowledge transfer, plus ongoing maintenance and enhancement.",
        "workflow_box_title": "Trusted Track Record",
        "workflow_box_subtitle": "Real solutions for measurable results",
        "workflow_box_bullet_1": "6+ production-ready systems at PT Pakarti Riken Indonesia",
        "workflow_box_bullet_2": "Specialized in manufacturing execution & quality management systems",
        "workflow_box_bullet_3": "Full-stack capabilities: Web applications, workflow automation, data analytics",
        "workflow_box_bullet_4": "Kaizen-driven methodology for continuous improvement",
        "workflow_box_btn": "Start Project Discussion",
        "inquiry_title": "Share Your Vision",
        "inquiry_desc": "Tell us about your business challenges. Our team will craft a comprehensive proposal with detailed scope, solution architecture, and transparent investment estimates.",
        "inquiry_client": "Company Name",
        "inquiry_project": "Project Title",
        "inquiry_scope": "Requirements Description",
        "inquiry_scope_placeholder": "Example: Real-time production tracking for 3 assembly lines, SAP integration, analytics dashboard",
        "inquiry_budget": "Budget Estimate (Rp)",
        "inquiry_contact": "Email / WhatsApp",
        "inquiry_submit": "Request Proposal",
        "inquiry_box_title": "Transparent & Professional Process",
        "inquiry_box_desc": "After receiving your inquiry, our team conducts thorough analysis and delivers a structured proposal in an easily accessible digital format.",
        "inquiry_box_bullet_1": "Proposal delivered via secure link with QR code for easy access",
        "inquiry_box_bullet_2": "Open on any device—desktop, tablet, or smartphone",
        "inquiry_box_bullet_3": "Modern interface with clear scope visualization and cost breakdown",
        "quotes_title": "Project Portfolio",
        "quotes_desc": "Systems we've developed for various manufacturing industry needs.",
        "quote_view": "Details",
        "footer_desc": "Engineering excellence for your industrial digital transformation.",
        "footer_capabilities": "Services",
        "footer_process": "Methodology",
        "footer_quotations": "Portfolio",
        "footer_contact": "Contact Us",
        "footer_meta": "Your trusted partner for manufacturing system innovation.",
        "quote_page_title": "Proposal Details",
        "quote_label_client": "Client",
        "quote_label_project": "Project",
        "quote_label_scope": "Scope of Work",
        "quote_label_amount": "Investment",
        "quote_label_status": "Status",
        "quote_label_created": "Date",
        "quote_copy_link": "Copy Link",
        "quote_invoice_btn": "Generate Invoice PDF",
        "quote_schedule_btn": "Schedule Meeting",
        "quote_qr_title": "Scan to open proposal",
        "admin_dashboard_title": "Admin Dashboard",
        "admin_highlights_title": "Service Highlights",
        "admin_inquiries_title": "Recent Inquiries",
        "admin_quotes_title": "Recent Proposals",
        "admin_logout": "Logout",
        "admin_add_new": "Add New",
        "admin_edit": "Edit",
        "admin_delete": "Delete",
    },
    "jp": {
        "nav_services": "サービス",
        "nav_workflow": "ワークフロー",
        "nav_quotes": "見積",
        "nav_admin": "管理",
        "hero_eyebrow": "エンジニアリング&システム開発ソリューション",
        "hero_title": "Prime Projectx",
        "hero_desc": "インテリジェントなシステム統合により、製造業の生産性を加速します。ワークフローのデジタル化、統計的品質管理から包括的な管理プラットフォームまで—現代の産業要求に対応する精密設計。",
        "hero_btn_primary": "無料相談予約",
        "hero_btn_secondary": "実績を見る",
        "hero_metric_1": "稼働中システム",
        "hero_metric_2": "業界パートナー",
        "hero_metric_3": "サポート稼働率",
        "capabilities_title": "私たちの専門性",
        "capabilities_desc": "AI統合による製造業のデジタル変革のためのエンドツーエンドソリューション—文書自動化、品質管理のための機械学習から運用効率とデータ駆動型意思決定を促進する予測分析まで。",
        "workflow_title": "協働プロセス",
        "workflow_step_1": "発見と分析",
        "workflow_step_1_desc": "ビジネス課題を理解するための徹底的な議論、ステークホルダー要件のマッピング、技術的実現可能性の検証。",
        "workflow_step_2": "ソリューション設計",
        "workflow_step_2_desc": "スケーラブルなアーキテクチャ設計、最適化されたデータベースモデリング、直感的なワイヤーフレーム、既存システムとの統合戦略。",
        "workflow_step_3": "アジャイル開発",
        "workflow_step_3_desc": "AI支援コーディング、自動テスト、リアルタイムドキュメンテーション、チームとの定期的なレビューによる反復的な実装。コード最適化と品質保証のためのAIツールを活用。",
        "workflow_step_4": "品質保証",
        "workflow_step_4_desc": "エンドユーザーによる受入テスト、パフォーマンスストレステスト、セキュリティ強化、コンプライアンス検証。",
        "workflow_step_5": "展開とイネーブルメント",
        "workflow_step_5_desc": "計画的な展開戦略、包括的なユーザートレーニング、ナレッジトランスファー、継続的なメンテナンスと機能拡張。",
        "workflow_box_title": "信頼の実績",
        "workflow_box_subtitle": "測定可能な成果のための実際のソリューション",
        "workflow_box_bullet_1": "PT Pakarti Riken Indonesiaで6つ以上の本番稼働システム",
        "workflow_box_bullet_2": "製造実行および品質管理システムに特化",
        "workflow_box_bullet_3": "フルスタック能力：Webアプリケーション、ワークフロー自動化、データ分析",
        "workflow_box_bullet_4": "継続的改善のための改善駆動型方法論",
        "workflow_box_btn": "プロジェクト相談開始",
        "inquiry_title": "ビジョンを共有",
        "inquiry_desc": "ビジネス課題についてお聞かせください。詳細なスコープ、ソリューションアーキテクチャ、透明な投資見積もりを含む包括的な提案を作成します。",
        "inquiry_client": "会社名",
        "inquiry_project": "プロジェクトタイトル",
        "inquiry_scope": "要件説明",
        "inquiry_scope_placeholder": "例：3つの組立ラインのリアルタイム生産追跡、SAP統合、分析ダッシュボード",
        "inquiry_budget": "予算見積 (Rp)",
        "inquiry_contact": "Email / WhatsApp",
        "inquiry_submit": "提案を依頼",
        "inquiry_box_title": "透明でプロフェッショナルなプロセス",
        "inquiry_box_desc": "お問い合わせを受け取った後、チームが徹底的な分析を行い、アクセスしやすいデジタル形式で構造化された提案を提供します。",
        "inquiry_box_bullet_1": "簡単にアクセスできるQRコード付きの安全なリンクで提案を配信",
        "inquiry_box_bullet_2": "デスクトップ、タブレット、スマートフォンなど、あらゆるデバイスで開けます",
        "inquiry_box_bullet_3": "明確なスコープの可視化とコスト内訳を備えたモダンなインターフェース",
        "quotes_title": "プロジェクトポートフォリオ",
        "quotes_desc": "様々な製造業のニーズに対して開発したシステム。",
        "quote_view": "詳細",
        "footer_desc": "産業デジタル変革のためのエンジニアリングエクセレンス。",
        "footer_capabilities": "サービス",
        "footer_process": "方法論",
        "footer_quotations": "ポートフォリオ",
        "footer_contact": "お問い合わせ",
        "footer_meta": "製造システムイノベーションの信頼できるパートナー。",
        "quote_page_title": "提案詳細",
        "quote_label_client": "クライアント",
        "quote_label_project": "プロジェクト",
        "quote_label_scope": "作業範囲",
        "quote_label_amount": "投資額",
        "quote_label_status": "ステータス",
        "quote_label_created": "日付",
        "quote_copy_link": "リンクをコピー",
        "quote_invoice_btn": "請求書PDFを生成",
        "quote_schedule_btn": "ミーティング予約",
        "quote_qr_title": "スキャンして提案を開く",
        "admin_dashboard_title": "管理ダッシュボード",
        "admin_highlights_title": "サービスハイライト",
        "admin_inquiries_title": "最近の問い合わせ",
        "admin_quotes_title": "最近の提案",
        "admin_logout": "ログアウト",
        "admin_add_new": "新規追加",
        "admin_edit": "編集",
        "admin_delete": "削除",
    }
}

# Helper functions for Firestore
def doc_to_dict(doc):
    """Convert Firestore document to dictionary with id"""
    if not doc.exists:
        return None
    data = doc.to_dict()
    data['id'] = doc.id
    # Keep created_at as datetime object for template formatting
    return data

def generate_token():
    """Generate unique token for quotes"""
    return secrets.token_urlsafe(10)

def get_lang():
    """Get current language from session, default to 'id'"""
    return session.get("lang", "id")

def get_text(key):
    """Get translated text for current language"""
    lang = get_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS["id"]).get(key, key)

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_auth"):
            flash("Silakan login sebagai admin.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# ===== PUBLIC ROUTES =====
@app.route("/set_lang/<lang>")
def set_lang(lang):
    """Set language preference"""
    if lang in ["id", "en", "jp"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("home"))

@app.route("/")
def home():
    # Get highlights from Firestore
    highlights_ref = db.collection('highlights').order_by('display_order').limit(6)
    highlights_docs = highlights_ref.stream()
    highlights = [doc_to_dict(doc) for doc in highlights_docs]
    
    # Get quotes from Firestore
    quotes_ref = db.collection('quotes').order_by('created_at', direction=firestore.Query.DESCENDING).limit(6)
    quotes_docs = quotes_ref.stream()
    quotes = [doc_to_dict(doc) for doc in quotes_docs]
    
    return render_template(
        "index.html",
        highlights=highlights,
        quotes=quotes,
        t=get_text,
        lang=get_lang()
    )

@app.route("/inquiries", methods=["POST"])
def create_inquiry():
    client_name = request.form.get("client_name", "").strip()
    project_name = request.form.get("project_name", "").strip()
    scope = request.form.get("scope", "").strip()
    contact = request.form.get("contact", "").strip()
    budget_raw = request.form.get("budget", "").strip()
    
    if not all([client_name, project_name, scope, contact]):
        flash("Semua field wajib diisi.", "error")
        return redirect(url_for("home"))
    
    budget = None
    if budget_raw:
        try:
            budget = float(budget_raw.replace(",", ""))
        except ValueError:
            pass
    
    # Save to Firestore
    inquiry_data = {
        'client_name': client_name,
        'project_name': project_name,
        'scope': scope,
        'contact': contact,
        'budget': budget,
        'status': 'New',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('inquiries').add(inquiry_data)
    
    flash("Pengajuan berhasil dikirim. Tim kami akan menghubungi Anda.", "success")
    return redirect(url_for("home"))

@app.route("/p/<quote_id>")
def view_public_quote(quote_id):
    # Public view accessed from portfolio list
    quote_ref = db.collection('quotes').document(quote_id)
    quote_doc = quote_ref.get()
    
    if not quote_doc.exists:
        abort(404)
    
    quote = doc_to_dict(quote_doc)
    if quote.get('token'):
        quote['url'] = url_for("view_quote", token=quote['token'], _external=True)
    
    return render_template(
        "quotation.html",
        quote=quote,
        is_full_access=False,
        t=get_text,
        lang=get_lang()
    )

@app.route("/q/<token>")
def view_quote(token):
    # Private view accessed via QR code / direct link
    # Find quote by token in Firestore
    quotes_ref = db.collection('quotes').where('token', '==', token).limit(1)
    quotes = list(quotes_ref.stream())
    
    if not quotes:
        abort(404)
    
    quote = doc_to_dict(quotes[0])
    quote['url'] = url_for("view_quote", token=token, _external=True)
    
    return render_template(
        "quotation.html",
        quote=quote,
        is_full_access=True,
        t=get_text,
        lang=get_lang()
    )

@app.route("/qr/<token>")
def qr_image(token):
    # Find quote by token
    quotes_ref = db.collection('quotes').where('token', '==', token).limit(1)
    quotes = list(quotes_ref.stream())
    
    if not quotes:
        abort(404)
    
    link = url_for("view_quote", token=token, _external=True)
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00eaff", back_color="#0a0f1a")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/invoice/<token>")
def invoice_pdf(token):
    # Generate a simple PDF invoice for the quote token
    quotes_ref = db.collection('quotes').where('token', '==', token).limit(1)
    quotes = list(quotes_ref.stream())

    if not quotes:
        abort(404)

    quote = doc_to_dict(quotes[0])
    project_name = quote.get('project_name', 'proposal')
    client_name = quote.get('client_name', 'Client')
    amount = quote.get('amount') or 0
    created_at = quote.get('created_at')
    status = quote.get('status', 'PROPOSAL')

    def rupiah(val):
        try:
            return f"Rp {val:,.0f}".replace(",", ".")
        except Exception:
            return "Rp -"

    def wrap_lines(text, width=90):
        text = text or "-"
        lines = []
        for para in str(text).split("\n"):
            para = para.strip()
            if not para:
                lines.append("")
                continue
            wrapped = textwrap.wrap(para, width=width) or [""]
            lines.extend(wrapped)
        return lines

    buf = io.BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    margin_left = 45
    margin_right = width - 45
    y = height - 40
    page_num = 1
    
    # GMT+7 timezone
    gmt7 = timezone(timedelta(hours=7))
    current_time = datetime.now(gmt7).strftime('%Y-%m-%d %H:%M WIB')

    def draw_page_number():
        pdf.setFont("Helvetica", 8)
        pdf.setFillColorRGB(0.5, 0.5, 0.5)
        pdf.drawRightString(margin_right, 20, f"Page {page_num}")
        pdf.setFillColorRGB(0, 0, 0)

    def ensure_space(current_y, min_y=100):
        nonlocal page_num
        if current_y < min_y:
            draw_page_number()
            pdf.showPage()
            page_num += 1
            # Redraw header on new page
            new_y = draw_header(height - 40)
            return new_y
        return current_y

    def draw_header(start_y):
        # Company branding with image header
        header_path = os.path.join(os.path.dirname(__file__), 'header invoice.png')
        if os.path.exists(header_path):
            try:
                img = ImageReader(header_path)
                # Draw image with full width
                img_width = margin_right - margin_left
                img_height = 70
                pdf.drawImage(img, margin_left, start_y - img_height, width=img_width, height=img_height, preserveAspectRatio=True, mask='auto')
                
                # Thin line separator
                pdf.setLineWidth(0.5)
                pdf.setStrokeColorRGB(0.85, 0.85, 0.85)
                pdf.line(margin_left, start_y - img_height - 8, margin_right, start_y - img_height - 8)
                pdf.setStrokeColorRGB(0, 0, 0)
                
                return start_y - img_height - 18
            except Exception:
                pass
        
        # Fallback: professional text-based header
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(margin_left, start_y, "Prime Projectx")
        
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.setFillColorRGB(0.4, 0.4, 0.4)
        pdf.drawString(margin_left, start_y - 18, "Engineering & System Development Solutions")
        pdf.setFillColorRGB(0, 0, 0)
        
        # Contact info - clean layout
        pdf.setFont("Helvetica", 7.5)
        pdf.setFillColorRGB(0.3, 0.3, 0.3)
        contact_x = margin_right - 165
        pdf.drawString(contact_x, start_y - 2, f"WhatsApp: {CONTACT_WHATSAPP}")
        pdf.drawString(contact_x, start_y - 12, f"Email: {CONTACT_EMAIL}")
        pdf.drawString(contact_x, start_y - 22, "LinkedIn: linkedin.com/in/galihprime")
        pdf.drawString(contact_x, start_y - 32, "Fastwork: fastwork.id/user/glh_prima")
        pdf.setFillColorRGB(0, 0, 0)
        
        # Elegant separator line
        pdf.setLineWidth(0.5)
        pdf.setStrokeColorRGB(0.85, 0.85, 0.85)
        pdf.line(margin_left, start_y - 44, margin_right, start_y - 44)
        pdf.setStrokeColorRGB(0, 0, 0)
        
        return start_y - 56

    def draw_line_separator(current_y, width_line=0.5, color=(0.9, 0.9, 0.9)):
        pdf.setLineWidth(width_line)
        pdf.setStrokeColorRGB(*color)
        pdf.line(margin_left, current_y, margin_right, current_y)
        pdf.setStrokeColorRGB(0, 0, 0)
        return current_y - 14

    def draw_block(title, body, current_y, title_font="Helvetica-Bold", body_font="Helvetica", wrap_width=100):
        current_y = ensure_space(current_y, min_y=120)
        
        # Professional section title
        pdf.setFillColorRGB(0.98, 0.98, 0.98)
        pdf.rect(margin_left - 3, current_y - 5, margin_right - margin_left + 6, 20, fill=1, stroke=0)
        
        pdf.setFillColorRGB(0.15, 0.15, 0.15)
        pdf.setFont(title_font, 10)
        pdf.drawString(margin_left + 2, current_y, title.upper())
        pdf.setFillColorRGB(0, 0, 0)
        current_y -= 24
        
        # Body text with proper spacing
        pdf.setFont(body_font, 9)
        pdf.setFillColorRGB(0.2, 0.2, 0.2)
        for line in wrap_lines(body, width=wrap_width):
            current_y = ensure_space(current_y, min_y=90)
            pdf.drawString(margin_left + 6, current_y, line)
            current_y -= 14
        
        pdf.setFillColorRGB(0, 0, 0)
        current_y = draw_line_separator(current_y - 3)
        return current_y

    # Draw header
    y = draw_header(y)

    # Professional invoice title section
    pdf.setFillColorRGB(0.08, 0.08, 0.15)
    pdf.rect(margin_left - 3, y - 54, margin_right - margin_left + 6, 54, fill=1, stroke=0)
    
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(margin_left + 8, y - 20, "INVOICE / PROPOSAL")
    
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(margin_left + 8, y - 36, f"Status: {status}  |  Generated: {current_time}")
    if created_at:
        pdf.drawString(margin_left + 8, y - 48, f"Proposal Date: {created_at}")
    
    pdf.setFillColorRGB(0, 0, 0)
    y -= 66
    
    y = draw_line_separator(y, 1, (0.8, 0.8, 0.8))

    # Bill to & Project in side-by-side boxes
    box_y = y
    
    # Bill To box
    pdf.setFillColorRGB(0.99, 0.99, 0.99)
    pdf.setStrokeColorRGB(0.85, 0.85, 0.85)
    pdf.rect(margin_left - 3, box_y - 50, (margin_right - margin_left) / 2 - 5, 50, fill=1, stroke=1)
    pdf.setStrokeColorRGB(0, 0, 0)
    
    pdf.setFillColorRGB(0.2, 0.2, 0.2)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(margin_left + 3, box_y - 14, "BILL TO")
    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(margin_left + 3, box_y - 30, client_name)
    
    # Project box
    project_x = margin_left + (margin_right - margin_left) / 2 + 5
    pdf.setFillColorRGB(0.97, 0.99, 1)
    pdf.setStrokeColorRGB(0.85, 0.85, 0.85)
    pdf.rect(project_x - 3, box_y - 50, (margin_right - margin_left) / 2 - 5, 50, fill=1, stroke=1)
    pdf.setStrokeColorRGB(0, 0, 0)
    
    pdf.setFillColorRGB(0.2, 0.2, 0.2)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(project_x + 3, box_y - 14, "PROJECT")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.setFillColorRGB(0, 0, 0)
    
    # Wrap project name if too long
    max_proj_width = (margin_right - project_x) - 12
    proj_words = project_name.split()
    proj_lines = []
    current_line = ""
    for word in proj_words:
        test_line = current_line + " " + word if current_line else word
        if pdf.stringWidth(test_line, "Helvetica-Bold", 11) < max_proj_width:
            current_line = test_line
        else:
            if current_line:
                proj_lines.append(current_line)
            current_line = word
    if current_line:
        proj_lines.append(current_line)
    
    proj_y = box_y - 30
    for proj_line in proj_lines[:2]:  # Max 2 lines
        pdf.drawString(project_x + 3, proj_y, proj_line)
        proj_y -= 12
    
    y = box_y - 60
    y = draw_line_separator(y, 1, (0.8, 0.8, 0.8))

    # Sections with full details
    sections = [
        ("Scope of Work", quote.get('scope', '')),
        ("Technical Approach", quote.get('technical_approach', '')),
        ("Technology Stack", quote.get('tech_stack', '')),
        ("Deliverables", quote.get('deliverables', '')),
        ("Timeline", quote.get('timeline', '')),
        ("Team Structure", quote.get('team_structure', '')),
        ("Assumptions & Dependencies", quote.get('assumptions', '')),
        ("Payment Terms", quote.get('payment_terms', '')),
    ]

    for title, body in sections:
        y = draw_block(title, body, y)

    # Investment amount - elegant highlight box
    y = ensure_space(y, min_y=140)
    
    box_height = 64
    pdf.setFillColorRGB(0.98, 0.98, 0.98)
    pdf.setStrokeColorRGB(0.75, 0.75, 0.75)
    pdf.setLineWidth(1)
    pdf.rect(margin_left - 3, y - box_height + 10, margin_right - margin_left + 6, box_height, fill=1, stroke=1)
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setFillColorRGB(0, 0, 0)
    
    pdf.setFont("Helvetica-Bold", 10)
    pdf.setFillColorRGB(0.3, 0.3, 0.3)
    pdf.drawString(margin_left + 8, y - 14, "INVESTMENT AMOUNT")
    
    pdf.setFont("Helvetica-Bold", 26)
    pdf.setFillColorRGB(0.1, 0.1, 0.1)
    pdf.drawString(margin_left + 8, y - 44, rupiah(amount))
    pdf.setFillColorRGB(0, 0, 0)
    
    y -= box_height + 30

    # Professional footer
    y = ensure_space(y, min_y=120)
    y = draw_line_separator(y, 1, (0.8, 0.8, 0.8))
    
    pdf.setFillColorRGB(0.98, 0.98, 0.98)
    pdf.rect(margin_left - 3, y - 90, margin_right - margin_left + 6, 90, fill=1, stroke=0)
    pdf.setFillColorRGB(0, 0, 0)
    
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margin_left + 8, y - 16, "Prime Projectx")
    
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.setFillColorRGB(0.4, 0.4, 0.4)
    pdf.drawString(margin_left + 8, y - 28, "Engineering & System Development Solutions")
    
    pdf.setFont("Helvetica", 8)
    pdf.drawString(margin_left + 8, y - 44, f"Email: {CONTACT_EMAIL}  |  WhatsApp: {CONTACT_WHATSAPP}")
    pdf.drawString(margin_left + 8, y - 56, "LinkedIn: linkedin.com/in/galihprime")
    pdf.drawString(margin_left + 8, y - 68, "Fastwork Collaboration: fastwork.id/user/glh_prima")
    
    pdf.setFont("Helvetica-Oblique", 7.5)
    pdf.setFillColorRGB(0.5, 0.5, 0.5)
    pdf.drawString(margin_left + 8, y - 84, "Thank you for your trust in our services.")
    pdf.setFillColorRGB(0, 0, 0)

    draw_page_number()
    pdf.showPage()
    pdf.save()

    buf.seek(0)
    safe_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "_", "-")) or "proposal"
    filename = f"Invoice-{safe_name}.pdf"
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=filename)

# ===== ADMIN ROUTES =====
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_auth"):
        return redirect(url_for("admin_dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_auth"] = True
            session["admin_name"] = username
            flash("Login berhasil.", "success")
            return redirect(url_for("admin_dashboard"))
        
        flash("Kredensial salah.", "error")
    
    return render_template("admin_login.html", t=get_text, lang=get_lang())

@app.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    flash("Anda sudah logout.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    # Get recent quotes
    quotes_ref = db.collection('quotes').order_by('created_at', direction=firestore.Query.DESCENDING).limit(10)
    quotes = [doc_to_dict(doc) for doc in quotes_ref.stream()]
    
    # Get recent inquiries
    inquiries_ref = db.collection('inquiries').order_by('created_at', direction=firestore.Query.DESCENDING).limit(10)
    inquiries = [doc_to_dict(doc) for doc in inquiries_ref.stream()]
    
    # Get highlights
    highlights_ref = db.collection('highlights').order_by('display_order')
    highlights = [doc_to_dict(doc) for doc in highlights_ref.stream()]
    
    return render_template(
        "admin_dashboard.html",
        quotes=quotes,
        inquiries=inquiries,
        highlights=highlights,
        t=get_text,
        lang=get_lang()
    )

@app.route("/admin/quotes")
@admin_required
def admin_quotes():
    quotes_ref = db.collection('quotes').order_by('created_at', direction=firestore.Query.DESCENDING)
    quotes = [doc_to_dict(doc) for doc in quotes_ref.stream()]
    return render_template("admin_quotes.html", quotes=quotes, t=get_text, lang=get_lang())

@app.route("/admin/quotes/new", methods=["GET", "POST"])
@admin_required
def admin_new_quote():
    if request.method == "POST":
        return _save_quote(None)
    return render_template("admin_quote_form.html", quote=None, t=get_text, lang=get_lang())

@app.route("/admin/quotes/<quote_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit_quote(quote_id):
    quote_ref = db.collection('quotes').document(quote_id)
    quote_doc = quote_ref.get()
    
    if not quote_doc.exists:
        flash("Quote tidak ditemukan.", "error")
        return redirect(url_for("admin_dashboard"))
    
    if request.method == "POST":
        return _save_quote(quote_id)
    
    quote = doc_to_dict(quote_doc)
    return render_template("admin_quote_form.html", quote=quote, t=get_text, lang=get_lang())

@app.post("/admin/quotes/<quote_id>/delete")
@admin_required
def admin_delete_quote(quote_id):
    quote_ref = db.collection('quotes').document(quote_id)
    quote_ref.delete()
    flash("Quotation dihapus.", "success")
    return redirect(url_for("admin_dashboard"))

def _save_quote(quote_id=None):
    """Helper to save quote (create or update)"""
    client_name = request.form.get("client_name", "").strip()
    project_name = request.form.get("project_name", "").strip()
    scope = request.form.get("scope", "").strip()
    amount_str = request.form.get("amount", "").strip()
    status = request.form.get("status", "Draft").strip() or "Draft"
    
    # Proposal fields
    technical_approach = request.form.get("technical_approach", "").strip()
    deliverables = request.form.get("deliverables", "").strip()
    timeline = request.form.get("timeline", "").strip()
    tech_stack = request.form.get("tech_stack", "").strip()
    team_structure = request.form.get("team_structure", "").strip()
    assumptions = request.form.get("assumptions", "").strip()
    payment_terms = request.form.get("payment_terms", "").strip()
    
    if not all([client_name, project_name, scope, amount_str]):
        flash("Field wajib: Client, Project, Scope, Amount.", "error")
        return redirect(request.referrer or url_for("admin_dashboard"))
    
    try:
        amount = float(amount_str.replace(",", ""))
    except ValueError:
        flash("Nominal tidak valid.", "error")
        return redirect(request.referrer or url_for("admin_dashboard"))
    
    quote_data = {
        'client_name': client_name,
        'project_name': project_name,
        'scope': scope,
        'amount': amount,
        'status': status,
        'technical_approach': technical_approach,
        'deliverables': deliverables,
        'timeline': timeline,
        'tech_stack': tech_stack,
        'team_structure': team_structure,
        'assumptions': assumptions,
        'payment_terms': payment_terms,
    }
    
    if quote_id:
        # Update existing
        quote_ref = db.collection('quotes').document(quote_id)
        quote_ref.update(quote_data)
        flash("Proposal berhasil disimpan!", "success")
    else:
        # Create new
        quote_data['token'] = generate_token()
        quote_data['created_at'] = firestore.SERVER_TIMESTAMP
        db.collection('quotes').add(quote_data)
        flash("Proposal berhasil disimpan! Link & QR code siap di-share.", "success")
    
    return redirect(url_for("admin_dashboard"))

# ===== HIGHLIGHTS ROUTES =====
@app.route("/admin/highlights/new", methods=["GET", "POST"])
@admin_required
def admin_new_highlight():
    if request.method == "POST":
        return _save_highlight(None)
    return render_template("admin_highlight_form.html", highlight=None, t=get_text, lang=get_lang())

@app.route("/admin/highlights/<highlight_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit_highlight(highlight_id):
    highlight_ref = db.collection('highlights').document(highlight_id)
    highlight_doc = highlight_ref.get()
    
    if not highlight_doc.exists:
        flash("Highlight tidak ditemukan.", "error")
        return redirect(url_for("admin_dashboard"))
    
    if request.method == "POST":
        return _save_highlight(highlight_id)
    
    highlight = doc_to_dict(highlight_doc)
    return render_template("admin_highlight_form.html", highlight=highlight, t=get_text, lang=get_lang())

@app.post("/admin/highlights/<highlight_id>/delete")
@admin_required
def admin_delete_highlight(highlight_id):
    highlight_ref = db.collection('highlights').document(highlight_id)
    highlight_ref.delete()
    flash("Highlight dihapus.", "success")
    return redirect(url_for("admin_dashboard"))

def _save_highlight(highlight_id=None):
    """Helper to save highlight (create or update)"""
    category = request.form.get("category", "").strip() or "General"
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    display_order_str = request.form.get("display_order", "0").strip()
    
    if not all([title, body]):
        flash("Title dan deskripsi wajib diisi.", "error")
        return redirect(request.referrer or url_for("admin_dashboard"))
    
    try:
        display_order = int(display_order_str or "0")
    except ValueError:
        display_order = 0
    
    highlight_data = {
        'category': category,
        'title': title,
        'body': body,
        'display_order': display_order
    }
    
    if highlight_id:
        # Update existing
        highlight_ref = db.collection('highlights').document(highlight_id)
        highlight_ref.update(highlight_data)
        flash("Highlight tersimpan.", "success")
    else:
        # Create new
        highlight_data['created_at'] = firestore.SERVER_TIMESTAMP
        db.collection('highlights').add(highlight_data)
        flash("Highlight tersimpan.", "success")
    
    return redirect(url_for("admin_dashboard"))

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html", t=get_text, lang=get_lang()), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5050"))
    host = os.environ.get("HOST", "127.0.0.1")
    app.run(debug=True, host=host, port=port)
