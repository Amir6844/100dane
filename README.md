# ۱۰۰دانه — 100dane

> **سامانه مدیریت آموزشی ایرانی** — هر کلاس، یک انار پر از دانه‌های دانش 🍎

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38BDF8?logo=tailwindcss)
![License](https://img.shields.io/badge/license-MIT-green)

**100dane** یک پلتفرم مدیریت کلاس ایرانی، سرور-رندر شده با Django + Tailwind CSS است — طراحی شده برای دبیران و دانش‌آموزان ایرانی با هویت فرهنگی انار، RTL کامل و تجربه کاربری پرمیوم SaaS.

[English](#english) | [فارسی](#فارسی)

---

<a id="فارسی"></a>
## ✨ ویژگی‌ها

- **کلاس** — ایجاد/ویرایش/حذف، سال تحصیلی، پایه، رشته، کاور، رنگ، کد دعوت ۶ حرفی، فعال/غیرفعال، داشبورد با میانگین و رتبه‌بندی
- **گروه‌بندی** — گروه با رنگ/ظرفیت/توضیحات، افزودن/حذف/جابه‌جایی اعضا، جلوگیری از تکراری و اعتبارسنجی عضویت کلاسی
- **دانش‌آموزان** — فهرست روستر (کد دانش‌آموزی/موبایل/یادداشت) + دانش‌آموزان عضو (User)، پروفایل با میانگین/بیشترین/کمترین/تعداد آزمون
- **درس** — گروه اختیاری، تاریخ، تکالیف (homework)، فایل پیوست، ترتیب
- **آزمون** — گروه اختیاری، درس مرتبط، حداکثر نمره (اعتبارسنجی ۰–۱۰۰)، نوع (کوییز/میان‌ترم/پایانی)
- **نمرات** — ثبت تکی + گروهی با `transaction.atomic`، اعتبارسنجی `0 ≤ نمره ≤ حداکثر`، جلوگیری از IDOR، نوتیفیکیشن
- **گزارش & Excel** — خروجی `.xlsx` با `openpyxl`، هدرهای فارسی `ردیف/نام/نام خانوادگی/کد دانش‌آموزی/گروه/آزمون/نمره/حداکثر نمره/درصد`، RTL و Vazirmatn، حالت‌ها: کلاس/گروه/آزمون/دانش‌آموز/تفصیلی
- **داشبورد** — معلم: آمار کلاس/دانش‌آموز/آزمون/میانگین + آخرین کلاس/آزمون • دانش‌آموز: کلاس‌های من + نمرات اخیر + گروه‌ها
- **احراز هویت** — نقش `teacher/student/admin`، login/logout، محافظت CSRF، مالکیت کلاس
- **نوتیفیکیشن** — اعلان عضویت/گروه/آزمون/نمره

## 🎨 طراحی

- **هویت:** انار — دانه‌های پراکنده، `seed-pattern`، `leaf-divider`، گرادیان `daneh-600 → barg-500`
- **رنگ:** `daneh` Pomegranate Red (#C22A4E), `barg` Persian Green, `gold`, `cream`/`ink`
- **تایپوگرافی:** Vazirmatn، سلسله‌مراتب پرمیوم، RTL-first (`dir="rtl"`)
- **لایه‌بندی:** Sidebar (راست، 285px، sticky) + Topbar + Main، Mobile drawer، `components/` و `partials/` قابل استفاده مجدد

## 🧱 معماری

```
config/          # settings, urls, wsgi
apps/
  accounts/      # User (role, phone, student_code, avatar), auth, persian filters
  classes/       # Classroom (academic_year, subject, is_active)
  students/      # Student roster (classroom FK, student_code)
  groups/        # Group (classroom FK, members M2M, description)
  lessons/       # Lesson (group FK, homework, lesson_date)
  exams/         # Exam (group FK, total_score, exam_date)
  scores/        # Score (exam+student, value, CheckConstraint), services.py
  notifications/ # Notification
templates/
  base.html + partials/sidebar.html + components/* + reports/dashboard.html
static/
```

## 🚀 نصب سریع

```bash
# 1. کلون
git clone https://github.com/<user>/100dane.git
cd 100dane

# 2. محیط مجازی
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. وابستگی‌ها
pip install -r requirements.txt
# Django==5.1 Pillow==11 openpyxl==3.1 django-crispy-forms crispy-tailwind django-jalali-date

# 4. مهاجرت
python manage.py migrate

# 5. داده دمو (اختیاری)
python manage.py seed_demo
# teacher / teacher123
# student1..8 / student123

# 6. اجرا
python manage.py runserver
# http://127.0.0.1:8000/
```

**PostgreSQL (اختیاری):**
```python
# config/settings.py -> uncomment DATABASES postgresql block
# export DB_NAME=daneh DB_USER=postgres DB_PASSWORD=... DB_HOST=localhost
```

## 👤 حساب‌ها

| نقش | نام کاربری | رمز |
|-----|------------|-----|
| دبیر | `teacher` | `teacher123` |
| دانش‌آموز | `student1` | `student123` |

## 📊 URL ها

```
/                         Landing
/accounts/login/          ورود
/accounts/register/       ثبت‌نام
/accounts/dashboard/      داشبورد
/classes/                 لیست کلاس
/classes/create/          ایجاد
/classes/<id>/            جزئیات + تب‌ها
/groups/class/<id>/create/ ایجاد گروه
/lessons/class/<id>/create/ ایجاد درس
/exams/class/<id>/create/  ایجاد آزمون
/scores/exam/<id>/bulk/   ثبت گروهی نمره
/scores/class/<id>/export/?mode=exam&exam=<id>  Excel
/reports/                 گزارش‌ها
```

## ✅ تست

```bash
python manage.py test --verbosity=2  # 41 tests
python manage.py check
```

پوشش: احراز هویت، مالکیت کلاس (IDOR 404)، CRUD کلاس/گروه/درس/آزمون، عضویت، نمره (منفی/>حداکثر)، bulk atomic، Excel هدر فارسی.

## 📦 Excel

`apps/scores/views.py:ExportExcelView` — `sheet_view.rightToLeft = True`, هدر پررنگ `C22A4E`, درصد محاسبه شده, نام فایل فارسی.

## 🌐 فارسی & RTL

`LANGUAGE_CODE='fa'`, `TIME_ZONE='Asia/Tehran'`, `dir="rtl"`, Vazirmatn CDN, `fa_digits`/`avg_color` فیلترها.

---

<a id="english"></a>
## English Overview

**100dane** (100 seeds) — Iranian classroom management, server-rendered Django + Tailwind, pomegranate brand.

**Stack:** Python 3.12, Django 5.1, SQLite (Postgres ready), Tailwind CDN, openpyxl, Pillow, crispy-tailwind.

**Quick start:** see Persian section above (`seed_demo` creates demo data, 41 tests).

**License:** MIT — for educational use. Change `SECRET_KEY` and `DEBUG` in production.

---

Made with ❤️ for Iranian education — انار دانش
