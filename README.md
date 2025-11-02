# Instagram Automation Tool

An open-source, self-hosted Instagram automation tool similar to ManyChat, designed to run without official API keys. It provides a backend API and a simple frontend interface to manage comment and DM automation tasks.

This project uses `instagrapi` for Instagram communication and can be deployed easily using Docker.

---

## Table of Contents

- [Features](#features)
- [Safety Features & Human-Like Behavior](#safety-features--human-like-behavior)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Docker (Recommended)](#docker-recommended)
  - [Manual Setup (venv)](#manual-setup-venv)
- [Making the Service Persistent (venv only)](#making-the-service-persistent-venv-only)
- [How to Use](#how-to-use)
- [API Documentation](#api-documentation)
- [Connecting with n8n (Advanced Tutorial)](#connecting-with-n8n-advanced-tutorial)
  - [Prerequisite: Logging In](#prerequisite-logging-in)
  - [Advanced Workflow: Smart, Rule-Based Comment Replies](#advanced-workflow-smart-rule-based-comment-replies)
- [Project Structure](#project-structure)
- [Farsi Documentation (مستندات فارسی)](#farsi-documentation-مستندات-فارسی)

---

## Features

- **DM & Comment Automation**: Automatically reply to comments and send DMs based on keywords.
- **Follower-Only Mode**: Restrict automation to only users who follow the page.
- **Customizable Replies**: Set multiple random replies for both comments and DMs.
- **No Official API Key Needed**: Works with private APIs via `instagrapi`.
- **Simple Web Interface**: Easy-to-use UI for managing your automation tasks.
- **Dockerized**: Quick and easy setup with Docker and Docker Compose.
- **n8n Integration**: A dedicated, flexible endpoint to connect with automation platforms like n8n.

## Safety Features & Human-Like Behavior

This tool has been designed with the safety of your Instagram account in mind. To avoid being flagged as a bot and to minimize the risk of action blocks, the following features have been implemented:

-   **Duplicate Reply Prevention**: The tool will not reply to a comment if it has already been answered (either by you or the bot). It checks if you have "liked" the comment, which Instagram does automatically when you reply.
-   **Random Delays**: Before posting any comment or sending a DM, the bot waits for a random period (between 5 to 15 seconds) to mimic human typing and response time.
-   **Variable Check Intervals**: The bot checks for new comments at variable intervals (between 60 to 100 seconds) instead of a fixed time, making its activity pattern less predictable.
-   **Efficient Follower Cache**: The list of your followers is cached for 30 minutes to dramatically reduce the number of API requests, which is a key factor in avoiding rate limits.

> **Disclaimer**: While these measures significantly increase safety, the use of any automation tool on Instagram carries inherent risks. Use it responsibly.

## How It Works

The application consists of two main parts:

1.  **Backend (FastAPI)**: A Python server that handles all the logic. It uses the `instagrapi` library to connect to Instagram.
2.  **Frontend (Vanilla JS/HTML/CSS)**: A simple user interface that runs in your browser.

## Installation

### Docker (Recommended)

**Prerequisites**: Docker & Docker Compose.

1.  **Clone the repository**.
2.  **Run setup script**: `./install.sh`.
3.  **Run containers**: `docker-compose up --build -d`.
4.  **Access**: Frontend at `http://localhost:<FRONTEND_PORT>` and API docs at `http://localhost:<BACKEND_PORT>/docs`.

> **✅ Service Persistence**: Docker services are configured with `restart: unless-stopped` and will restart automatically with the server.

### Manual Setup (venv)

1.  **Clone repository**.
2.  **Run setup script**: `./setup_venv.sh`.
3.  **Activate environment**: `source backend/.venv/bin/activate`.
4.  **Run servers** in separate terminals.

## Making the Service Persistent (venv only)

To make the `.venv` installation persistent across reboots, set it up as a `systemd` service. Templates and a full guide are in the Farsi documentation section, which applies to any Linux system.

## How to Use

### 1. Logging In
Use the UI to log in with your credentials or a session JSON.

### 2. Creating an Automation Task
Fill out the form in the UI to define the post, keywords, and replies for your automation.

### 3. Managing Tasks
View and delete active automations from the list in the UI.

## API Documentation

Full API documentation is available at the `/docs` endpoint of the backend.

-   **Authentication**: Endpoints for login, logout, and status check.
-   **Automation**: Endpoints to create, view, and delete automation tasks.
-   **n8n Integration**: A powerful `/api/n8n/action` endpoint supporting actions like `send_dm`, `post_comment`, `get_user_posts`, and `check_follower_status`.

## Connecting with n8n (Advanced Tutorial)
(This section is detailed in the Farsi translation below, which provides a universal step-by-step guide.)

---

# Farsi Documentation (مستندات فارسی)

## ابزار اتوماسیون اینستاگرام

یک ابزار اتوماسیون اینستاگرام متن-باز و سلف-هاست که مشابه ManyChat عمل می‌کند، با این تفاوت که نیازی به کلید API رسمی اینستاگرام ندارد.

### قابلیت‌ها
- **اتوماسیون دایرکت و کامنت**
- **حالت فقط فالوورها**
- **پاسخ‌های سفارشی و رندوم**
- **رابط کاربری ساده تحت وب**
- **نصب آسان با Docker**
- **اتصال به n8n**

### ویژگی‌های ایمنی و شبیه‌سازی رفتار انسانی

-   **جلوگیری از پاسخ تکراری**: با بررسی لایک شدن کامنت، از پاسخ مجدد جلوگیری می‌شود.
-   **تأخیرهای تصادفی**: قبل از هر پاسخ، یک تأخیر رندوم برای شبیه‌سازی رفتار انسان اعمال می‌شود.
-   **فواصل زمانی متغیر**: ربات در بازه‌های زمانی متغیر کامنت‌ها را چک می‌کند.
-   **کش بهینه فالوورها**: برای کاهش شدید تعداد درخواست‌ها به اینستاگرام، لیست فالوورها کش می‌شود.

> **سلب مسئولیت**: استفاده از هرگونه ابزار اتوماسیون با ریسک همراه است. با مسئولیت استفاده کنید.

### نصب و راه‌اندازی

#### روش اول: Docker (توصیه شده)
1.  **پروژه را دریافت کنید**.
2.  **اسکریپت نصب را اجرا کنید**: `./install.sh`.
3.  **کانتینرها را اجرا کنید**: `docker-compose up --build -d`.
4.  **دسترسی**: به `http://localhost:<FRONTEND_PORT>` مراجعه کنید.

> **✅ پایداری سرویس**: سرویس‌های داکر به صورت خودکار پس از ریبوت سرور اجرا می‌شوند.

#### روش دوم: نصب دستی (venv)
1.  **پروژه را دریافت کنید**.
2.  **اسکریپت نصب را اجرا کنید**: `./setup_venv.sh`.
3.  **محیط مجازی را فعال کنید** و سرورها را در ترمینال‌های جداگانه اجرا نمایید.

### پایدارسازی سرویس (فقط برای نصب با venv)

برای اجرای خودکار اپلیکیشن پس از ریبوت سرور در نصب دستی، باید از `systemd` استفاده کنید.

**راهنمای قدم به قدم**:

1.  **ویرایش فایل‌های الگو**: فایل‌های `deployment/insta-backend.service` و `deployment/insta-frontend.service` را باز کرده و `your_user` را با نام کاربری لینوکس خود و `/path/to/your/project` را با آدرس کامل پروژه جایگزین کنید.
2.  **کپی کردن فایل‌ها**:
    ```bash
    sudo cp deployment/insta-backend.service /etc/systemd/system/
    sudo cp deployment/insta-frontend.service /etc/systemd/system/
    ```
3.  **بارگذاری و فعال‌سازی سرویس‌ها**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable insta-backend.service insta-frontend.service
    sudo systemctl start insta-backend.service insta-frontend.service
    ```
4.  **بررسی وضعیت**: `sudo systemctl status insta-backend.service`.

### آموزش پیشرفته اتصال به n8n

این آموزش یک ورک‌فلو قدرتمند برای پاسخ هوشمند به کامنت‌ها با استفاده از Google Sheets و AI را شرح می‌دهد.

#### پیش‌نیاز: لاگین به اینستاگرام
یک ورک‌فلو مجزا و یک‌بار مصرف برای لاگین بسازید. توصیه می‌شود از روش **Session JSON** استفاده کنید.

```
+-------------------------------------------------------------------+
| [1] نود Manual Start (شروع دستی)                                  |
+-------------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------------+
| [2] نود HTTP Request: "ورود به اینستاگرام"                         |
+-------------------------------------------------------------------+
|   Request Method:    POST               (حالت: Fixed)            |
|   URL:               http://localhost:8000/login/session (حالت: Fixed) |
|   Body Content Type: JSON               (حالت: Fixed)            |
|   JSON/RAW:                                                       |
|     - Key: session_data, Value: { "sessionid": "...", ... }     |
+-------------------------------------------------------------------+
```
> **دستورالعمل**: این ورک‌فلو را یک بار اجرا کنید تا لاگین شوید.

#### ورک‌فلو پیشرفته: پاسخ هوشمند و قانون‌مند

**دیاگرام کلی ورک‌فلو**:
`[Cron] -> [Get Posts] -> [Split] -> [Get Comments] -> [Split] -> [Filter] -> [Read Sheet] -> [IF Rule?] -> ... (logic branches)`

**تنظیمات قدم به قدم نودها**:

1.  **نود Cron (شروع زمان‌بندی شده)**: هر ۱۵ دقیقه اجرا شود.
2.  **نود HTTP Request (دریافت آخرین پست‌ها)**: `action: get_user_posts`, `payload: { "amount": 5 }`.
3.  **نود HTTP Request (دریافت کامنت‌های پست)**: `action: get_media_comments`, `payload: { "media_id": "{{ $json.pk }}" }`.
4.  **نود Code (فیلتر کامنت‌های پاسخ داده شده)**: اگر `$json.has_liked` صحیح بود، `return null`.
5.  **نود Google Sheets (خواندن قوانین از شیت)**: یک ردیف را بر اساس `PostURL` جستجو کنید.
6.  **نود IF (قانون یافت شد؟)**: بررسی کنید آیا خروجی نود شیت خالی است یا خیر.
    -   **شاخه FALSE (بدون قانون)**: به نود **OpenAI** متصل شده و یک پاسخ هوشمند تولید می‌کند. سپس با یک نود **HTTP Request** (`action: post_comment`) پاسخ را ارسال می‌کند.
    -   **شاخه TRUE (قانون یافت شد)**:
        1.  **نود Code (بررسی تطابق کلمات کلیدی)**: متن کامنت را با کلمات کلیدی شیت مقایسه می‌کند.
        2.  **نود IF (تطابق دارد؟)**: اگر تطابق وجود داشت، ادامه می‌دهد.
        3.  **نود HTTP Request (بررسی وضعیت فالوور)**: `action: check_follower_status`, `payload: { "target_user_id": "{{ ... }}" }`.
        4.  **نود IF (آیا فالوور است؟)**: بر اساس وضعیت فالو و مقدار ستون `FollowerOnly` در شیت تصمیم می‌گیرد.
        5.  **نودهای HTTP Request نهایی**: بر اساس خروجی IF قبلی، یا `CommentReply` اصلی از شیت را ارسال می‌کنند، یا یک پیام جایگزین برای درخواست فالو.