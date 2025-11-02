# Instagram Automation Tool

This document provides a comprehensive guide to the Instagram Automation Tool, covering its features, installation, usage, and advanced integration with platforms like n8n.

---

<details>
<summary>🇮🇷 **فهرست مطالب (برای باز شدن کلیک کنید)**</summary>

1.  [معرفی پروژه](#معرفی-پروژه)
2.  [قابلیت‌های کلیدی](#قابلیت-های-کلیدی)
3.  [ویژگی‌های ایمنی و شبیه‌سازی رفتار انسانی](#ویژگی-های-ایمنی-و-شبیه-سازی-رفتار-انسانی)
4.  [راهنمای نصب](#راهنمای-نصب)
    *   [پیش‌نیازها](#پیش-نیازها)
    *   [نصب با Docker (روش پیشنهادی)](#نصب-با-docker-روش-پیشنهادی)
    *   [نصب با محیط مجازی پایتون (venv)](#نصب-با-محیط-مجازی-پایتون-venv)
5.  [پایدارسازی سرویس (فقط برای نصب با venv)](#پایدارسازی-سرویس-فقط-برای-نصب-با-venv)
6.  [راهنمای استفاده (رابط کاربری وب)](#راهنمای-استفاده-رابط-کاربری-وب)
7.  [مستندات API](#مستندات-api)
    *   [ورود به سیستم (Login)](#ورود-به-سیستم-login)
    *   [مدیریت وظایف (Tasks)](#مدیریت-وظایف-tasks)
    *   [اندپوینت اختصاصی n8n](#اندپوینت-اختصاصی-n8n)
8.  [آموزش پیشرفته اتصال به n8n](#آموزش-پیشرفته-اتصال-به-n8n)
    *   [سناریوی نهایی](#سناریوی-نهایی)
    *   [مراحل پیاده‌سازی در n8n](#مراحل-پیاده-سازی-در-n8n)
9.  [پرسش و پاسخ‌های متداول](#پرسش-و-پاسخ-های-متداول)
10. [ساختار پروژه](#ساختار-پروژه)

</details>

<details>
<summary>🇬🇧 **Table of Contents (Click to expand)**</summary>

1.  [Introduction](#introduction)
2.  [Core Features](#core-features)
3.  [Safety Features & Human-Like Behavior](#safety-features--human-like-behavior)
4.  [Installation Guide](#installation-guide)
    *   [Prerequisites](#prerequisites)
    *   [Installation with Docker (Recommended)](#installation-with-docker-recommended)
    *   [Installation with Python Virtual Environment (venv)](#installation-with-python-virtual-environment-venv)
5.  [Making the Service Persistent (venv only)](#making-the-service-persistent-venv-only)
6.  [Usage Guide (Web UI)](#usage-guide-web-ui)
7.  [API Documentation](#api-documentation)
    *   [Login](#login-1)
    *   [Task Management](#task-management)
    *   [Dedicated n8n Endpoint](#dedicated-n8n-endpoint)
8.  [Advanced n8n Tutorial](#advanced-n8n-tutorial)
    *   [The Final Scenario](#the-final-scenario)
    *   [Implementation Steps in n8n](#implementation-steps-in-n8n)
9.  [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
10. [Project Structure](#project-structure)

</details>

---

# 🇮🇷 مستندات فارسی

## ۱. معرفی پروژه
این پروژه یک ابزار اتوماسیون اینستاگرام متن-باز و قابل میزبانی روی سرور شخصی (سلف-هاست) است که برای مدیریت خودکار کامنت‌ها و دایرکت‌ها طراحی شده است. هدف اصلی این ابزار، ارائه قابلیت‌هایی مشابه سرویس‌های پولی مانند ManyChat، بدون نیاز به API رسمی و هزینه‌بر اینستاگرام است. این ابزار با استفاده از کتابخانه `instagrapi` ساخته شده و دارای یک رابط کاربری وب ساده برای مدیریت آسان وظایف اتوماسیون است.

## ۲. قابلیت‌های کلیدی
-   **رابط کاربری وب**: مدیریت آسان وظایف اتوماسیون از طریق یک پنل تحت وب.
-   **ورود امن**: پشتیبانی از ورود با نام کاربری و رمز عبور یا `sessionid`.
-   **اتوماسیون کامنت‌ها**: پاسخ خودکار به کامنت‌ها بر اساس کلمات کلیدی مشخص.
-   **اتوماسیون دایرکت (DM)**: ارسال پیام خودکار به کاربرانی که کامنت خاصی را درج می‌کنند.
-   **بررسی وضعیت فالو**: امکان تنظیم شرط برای پاسخ‌دهی (مثلاً فقط به فالوورها پاسخ داده شود).
-   **نصب آسان**: اسکریپت‌های نصب هوشمند برای Docker و محیط مجازی پایتون (venv).
-   **پیکربندی پورت‌ها**: قابلیت تنظیم پورت‌های برنامه به صورت دستی یا استفاده از مقادیر پیش‌فرض.
-   **ادغام با n8n**: اندپوینت اختصاصی برای اتصال و اجرای سناریوهای پیچیده در n8n.

## ۳. ویژگی‌های ایمنی و شبیه‌سازی رفتار انسانی
برای جلوگیری از شناسایی شدن به عنوان ربات و مسدود شدن حساب کاربری، چندین ویژگی ایمنی در این ابزار تعبیه شده است:
-   **تأخیرهای تصادفی**: قبل از انجام هر عملیات (مانند لایک، کامنت، یا دایرکت)، یک تأخیر تصادفی کوتاه اعمال می‌شود تا رفتار طبیعی‌تر به نظر برسد.
-   **وقفه‌های متغیر**: فاصله زمانی بین هر بار بررسی پست‌ها برای کامنت‌های جدید، به صورت متغیر و در یک بازه زمانی مشخص (مثلاً بین ۶۰ تا ۱۲۰ ثانیه) تنظیم شده است.
-   **حافظه پنهان (Cache) فالوورها**: برای کاهش تعداد درخواست‌ها به سرور اینستاگرام، لیست فالوورهای کاربر به مدت مشخصی (مثلاً ۱۰ دقیقه) در حافظه پنهان نگهداری می‌شود. این کار از API Rate Limiting جلوگیری می‌کند.
-   **جلوگیری از پاسخ تکراری**: سیستم با بررسی اینکه آیا یک کامنت قبلاً لایک شده است (`comment.has_liked`)، از پاسخ دادن مجدد به آن جلوگیری می‌کند.

## ۴. راهنمای نصب

### پیش‌نیازها
-   سرور مجازی (VPS) با سیستم‌عامل Ubuntu 20.04 یا بالاتر.
-   حداقل ۱ گیگابایت رم.
-   نصب بودن `git` روی سرور.
-   برای نصب با Docker: نصب بودن `Docker` و `Docker Compose`.
-   برای نصب با venv: نصب بودن `Python 3.9` یا بالاتر.

### نصب با Docker (روش پیشنهادی)
این روش ساده‌ترین و پایدارترین راه برای اجرای برنامه است.

**مرحله ۱: کلون کردن پروژه**
ابتدا وارد سرور خود شوید و دستور زیر را برای دریافت سورس کد پروژه اجرا کنید:
```bash
git clone https://github.com/your-username/instagram-automation.git
cd instagram-automation
```

**مرحله ۲: اجرای اسکریپت نصب**
اسکریپت نصب را با دسترسی اجرایی کرده و آن را اجرا کنید:
```bash
chmod +x install.sh
./install.sh
```
اسکریپت از شما سوالات زیر را خواهد پرسید:
1.  `Do you want to set ports manually? (y/n)`: آیا می‌خواهید پورت‌ها را دستی تنظیم کنید؟
    -   اگر `n` را وارد کنید، پورت‌های پیش‌فرض (`8000` برای Backend و `8080` برای Frontend) استفاده خواهند شد.
    -   اگر `y` را وارد کنید، اسکریپت از شما می‌خواهد که پورت مورد نظر برای Backend و Frontend را وارد کنید.

پس از پاسخ به سوالات، اسکریپت به طور خودکار فایل‌های Docker Compose را پیکربندی کرده و کانتینرها را ساخته و اجرا می‌کند.

**مرحله ۳: دسترسی به برنامه**
پس از اتمام نصب، می‌توانید از طریق آدرس `http://<YOUR_SERVER_IP>:<FRONTEND_PORT>` به رابط کاربری وب دسترسی پیدا کنید.

### نصب با محیط مجازی پایتون (venv)
این روش برای کاربرانی که می‌خواهند کنترل بیشتری روی محیط اجرایی داشته باشند، مناسب است.

**مرحله ۱: کلون کردن پروژه**
```bash
git clone https://github.com/your-username/instagram-automation.git
cd instagram-automation
```

**مرحله ۲: اجرای اسکریپت نصب venv**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```
این اسکریپت نیز مشابه اسکریپت Docker، سوالاتی در مورد تنظیم پورت‌ها از شما خواهد پرسید و سپس:
-   یک محیط مجازی پایتون در پوشه `.venv` ایجاد می‌کند.
-   بسته‌های نرم‌افزاری مورد نیاز را از `requirements.txt` نصب می‌کند.
-   سرویس‌های Backend و Frontend را در پس‌زمینه اجرا می‌کند.

**مرحله ۳: دسترسی به برنامه**
مانند روش Docker، برنامه از طریق `http://<YOUR_SERVER_IP>:<FRONTEND_PORT>` در دسترس خواهد بود.

## ۵. پایدارسازی سرویس (فقط برای نصب با venv)
در صورتی که از روش `venv` استفاده کرده‌اید، سرویس‌ها پس از ریبوت شدن سرور به طور خودکار اجرا نخواهند شد. برای پایدارسازی سرویس‌ها، می‌توانید از `systemd` استفاده کنید.

**مرحله ۱: ایجاد فایل‌های سرویس**
دو فایل سرویس برای Backend و Frontend ایجاد کنید.

**فایل `backend.service`:**
```bash
sudo nano /etc/systemd/system/insta_backend.service
```
محتوای زیر را داخل فایل قرار دهید. **توجه:** مسیرهای `WorkingDirectory` و `ExecStart` را با مسیر واقعی پروژه خود جایگزین کنید.
```ini
[Unit]
Description=Instagram Automation Backend Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/instagram-automation/backend
ExecStart=/root/instagram-automation/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**فایل `frontend.service`:**
```bash
sudo nano /etc/systemd/system/insta_frontend.service
```
محتوای زیر را داخل فایل قرار دهید و مسیرها را مطابق با پروژه خود تنظیم کنید.
```ini
[Unit]
Description=Instagram Automation Frontend Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/instagram-automation/frontend
ExecStart=/root/instagram-automation/.venv/bin/python -m http.server 8080
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**مرحله ۲: فعال‌سازی و اجرای سرویس‌ها**
دستورات زیر را برای فعال‌سازی و اجرای سرویس‌ها اجرا کنید:
```bash
sudo systemctl daemon-reload
sudo systemctl enable insta_backend.service
sudo systemctl start insta_backend.service
sudo systemctl enable insta_frontend.service
sudo systemctl start insta_frontend.service
```
برای بررسی وضعیت سرویس‌ها می‌توانید از دستور `sudo systemctl status insta_backend.service` استفاده کنید.

## ۶. راهنمای استفاده (رابط کاربری وب)
۱.  **ورود**: در صفحه اول، نام کاربری و رمز عبور اکانت اینستاگرام خود را وارد کرده و روی دکمه "Login" کلیک کنید.
۲.  **مدیریت وظایف**: پس از ورود موفق، به صفحه مدیریت وظایف هدایت می‌شوید.
    -   **Add Task**: برای افزودن یک وظیفه جدید، فرم را پر کنید:
        -   **Post URL**: لینک کامل پستی که می‌خواهید زیر آن اتوماسیون انجام شود.
        -   **Keywords**: کلمات کلیدی که کامنت باید شامل آن‌ها باشد (با کاما جدا کنید).
        -   **Reply Message**: پیامی که در پاسخ به کامنت ارسال می‌شود.
        -   **DM Message**: پیامی که به دایرکت کاربر ارسال می‌شود (اختیاری).
        -   **Must Follow**: اگر تیک این گزینه را بزنید، اتوماسیون فقط برای فالوورهای شما اجرا می‌شود.
    -   **لیست وظایف**: وظایف فعال در جدولی نمایش داده می‌شوند. می‌توانید هر وظیفه را حذف کنید.

## ۷. مستندات API
تمامی اندپوینت‌ها از آدرس `http://<YOUR_SERVER_IP>:<BACKEND_PORT>` قابل دسترس هستند.

### ورود به سیستم (Login)
-   **URL**: `/api/login`
-   **Method**: `POST`
-   **Body**:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
-   **Success Response (200)**:
    ```json
    {
      "message": "Logged in successfully",
      "sessionid": "returned_session_id"
    }
    ```

### مدیریت وظایف (Tasks)
-   **Get All Tasks**:
    -   **URL**: `/api/tasks`
    -   **Method**: `GET`
-   **Add a Task**:
    -   **URL**: `/api/tasks`
    -   **Method**: `POST`
    -   **Body**:
        ```json
        {
          "post_url": "https://www.instagram.com/p/Cxyz...",
          "keywords": "test,hello",
          "reply_message": "Thanks for your comment!",
          "dm_message": "Hello from automation!",
          "must_follow": true
        }
        ```
-   **Delete a Task**:
    -   **URL**: `/api/tasks/{task_id}`
    -   **Method**: `DELETE`

### اندپوینت اختصاصی n8n
این اندپوینت برای اجرای عملیات‌های مختلف از طریق n8n طراحی شده است.

-   **URL**: `/api/n8n/action`
-   **Method**: `POST`
-   **Headers**:
    -   `Authorization`: `Bearer <YOUR_JWT_TOKEN>` (این توکن همان `sessionid` است که از اندپوینت لاگین دریافت شده)
-   **Body**:
    ```json
    {
      "action": "action_name",
      "params": { ... }
    }
    ```
-   **اقدامات (Actions) موجود**:
    1.  `check_follower_status`: بررسی می‌کند که آیا یک کاربر، کاربر دیگری را فالو می‌کند یا نه.
        -   `params`: `{ "user_to_check": "username1", "user_to_check_against": "username2" }`
    2.  `get_user_posts`: آخرین پست‌های یک کاربر را برمی‌گرداند.
        -   `params`: `{ "username": "target_username", "count": 5 }`
    3.  `send_dm`: ارسال یک پیام دایرکت.
        -   `params`: `{ "username": "recipient_username", "message": "Your message here" }`

## ۸. آموزش پیشرفته اتصال به n8n
در این سناریو، یک ورک‌فلو در n8n می‌سازیم که به صورت خودکار به کاربرانی که زیر پست آخر شما کامنتی با یک کلمه کلیدی خاص می‌گذارند، پاسخ می‌دهد و در صورت نیاز، اطلاعات آن‌ها را در یک Google Sheet ذخیره کرده و از یک سرویس هوش مصنوعی برای تولید پاسخ استفاده می‌کند.

### سناریوی نهایی:
1.  ورک‌فلو هر ۵ دقیقه یک بار اجرا می‌شود.
2.  آخرین پست شما را از طریق اندپوینت `get_user_posts` دریافت می‌کند.
3.  کامنت‌های آن پست را بررسی می‌کند.
4.  اگر کامنتی حاوی کلمه کلیدی `ai` بود و قبلاً به آن پاسخ داده نشده بود:
    a. بررسی می‌کند که آیا کاربر کامنت‌گذار شما را فالو می‌کند (`check_follower_status`).
    b. اگر فالو می‌کرد، متن کامنت را به یک مدل زبان بزرگ (LLM) ارسال می‌کند تا یک پاسخ مناسب تولید شود.
    c. پاسخ تولید شده را به عنوان ریپلای به کامنت ارسال می‌کند.
    d. یک پیام تشکر به دایرکت کاربر ارسال می‌کند (`send_dm`).
    e. نام کاربری و متن کامنت را در یک Google Sheet ذخیره می‌کند.

### مراحل پیاده‌سازی در n8n

**(تصاویر و جزئیات دقیق‌تر در رابط کاربری n8n قابل مشاهده خواهد بود)**

**Node 1: Schedule Trigger**
-   این نود را طوری تنظیم کنید که ورک‌فلو هر ۵ دقیقه یک بار اجرا شود.

**Node 2: HTTP Request - Get Last Post**
-   **URL**: `http://<YOUR_SERVER_IP>:<BACKEND_PORT>/api/n8n/action`
-   **Method**: `POST`
-   **Authentication**: `Header Auth`
    -   **Name**: `Authorization`
    -   **Value**: `Bearer {{ $credentials.apiToken.token }}` (توکن خود را در Credentials ذخیره کنید)
-   **Body**:
    ```json
    {
      "action": "get_user_posts",
      "params": {
        "username": "your_instagram_username",
        "count": 1
      }
    }
    ```

**Node 3: Loop Over Comments**
-   از یک نود `Split in Batches` یا مشابه برای پردازش تک‌تک کامنت‌های دریافتی از نود قبلی استفاده کنید.

**Node 4: IF Node - Check for Keyword and Replied Status**
-   شرط اول: `{{ $json.text }}` -> `contains` -> `ai`
-   شرط دوم: `{{ $json.has_replied }}` -> `is` -> `false`

**Node 5: HTTP Request - Check Follower Status**
-   (متصل به خروجی `true` نود IF)
-   **URL**: `http://.../api/n8n/action`
-   **Method**: `POST`
-   **Body**:
    ```json
    {
      "action": "check_follower_status",
      "params": {
        "user_to_check": "{{ $json.owner.username }}",
        "user_to_check_against": "your_instagram_username"
      }
    }
    ```

**Node 6: IF Node - Is a Follower?**
-   شرط: `{{ $json.is_follower }}` -> `is` -> `true`

**Node 7: AI Agent / LLM Node**
-   (متصل به خروجی `true` نود قبلی)
-   از نود OpenAI یا هر سرویس دیگری استفاده کنید.
-   **Prompt**: `Generate a friendly and helpful reply to this Instagram comment: "{{ $json.text }}"`

**Node 8: HTTP Request - Reply to Comment**
-   (از اندپوینت `comment_reply` که در `instagrapi` وجود دارد استفاده کنید. این اندپوینت باید به پروژه اضافه شود یا از طریق یک اکشن سفارشی فراخوانی شود).
-   **URL**: `http://.../api/n8n/action`
-   **Body**:
    ```json
    {
      "action": "reply_to_comment",
      "params": {
        "comment_id": "{{ $json.pk }}",
        "message": "{{ $node['AI Agent'].json.response }}"
      }
    }
    ```

**Node 9: HTTP Request - Send DM**
-   **URL**: `http://.../api/n8n/action`
-   **Body**:
    ```json
    {
      "action": "send_dm",
      "params": {
        "username": "{{ $json.owner.username }}",
        "message": "Thanks for your great comment! I've replied to it."
      }
    }
    ```

**Node 10: Google Sheets Node**
-   اطلاعات کاربر (`username`, `comment text`) را در یک شیت جدید ذخیره کنید.

این ورک‌فلو یک مثال قدرتمند از چگونگی ترکیب این ابزار با n8n برای ایجاد اتوماسیون‌های هوشمند و پیچیده است.

## ۹. پرسش و پاسخ‌های متداول
**س: آیا استفاده از این ابزار امن است؟**
ج: بله. با استفاده از تأخیرهای تصادفی و مکانیسم‌های کش، تلاش شده تا رفتار برنامه تا حد ممکن به رفتار انسان نزدیک باشد. با این حال، همیشه ریسک محدودی در استفاده از ابزارهای اتوماسیون وجود دارد. توصیه می‌شود از این ابزار با احتیاط استفاده کنید.

**س: چرا گاهی اوقات برنامه کامنت‌ها را با تأخیر پاسخ می‌دهد؟**
ج: این بخشی از طراحی ایمنی برنامه است. وقفه‌های متغیر بین بررسی‌ها باعث می‌شود که فعالیت شما کمتر به عنوان ربات شناسایی شود.

**س: آیا می‌توانم این ابزار را روی ویندوز نصب کنم؟**
ج: بله، با نصب پایتون و دنبال کردن راهنمای venv، امکان‌پذیر است. اما برای اجرای پایدار، استفاده از سرور لینوکس با Docker توصیه می‌شود.

## ۱۰. ساختار پروژه
```
/
├── backend/
│   ├── main.py         # FastAPI application
│   ├── logic.py        # Core automation logic
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env.template       # Environment variables template
├── docker-compose.yml
├── install.sh          # Docker installation script
└── setup_venv.sh       # venv installation script
```

---

# 🇬🇧 English Documentation

## 1. Introduction
This project is a self-hostable, open-source Instagram automation tool designed for automatically managing comments and direct messages. Its primary goal is to offer functionalities similar to paid services like ManyChat, without requiring the official, costly Instagram API. The tool is built using the `instagrapi` library and features a simple web interface for easy management of automation tasks.

## 2. Core Features
-   **Web UI**: Easily manage automation tasks through a web-based panel.
-   **Secure Login**: Supports login via username/password or `sessionid`.
-   **Comment Automation**: Automatically reply to comments based on specified keywords.
-   **DM Automation**: Automatically send a direct message to users who leave a specific comment.
-   **Follower Check**: Set conditions for replies (e.g., respond only to followers).
-   **Easy Installation**: Smart installation scripts for both Docker and Python virtual environments (venv).
-   **Port Configuration**: Manually configure application ports or use default values.
-   **n8n Integration**: A dedicated endpoint for connecting and executing complex workflows in n8n.

## 3. Safety Features & Human-Like Behavior
To avoid being detected as a bot and getting your account banned, several safety features have been implemented:
-   **Random Delays**: A short, random delay is applied before performing any action (like, comment, or DM) to appear more natural.
-   **Variable Intervals**: The time between checking posts for new comments is variable, set within a specific range (e.g., 60 to 120 seconds).
-   **Follower Cache**: To reduce the number of requests to Instagram's servers, the user's follower list is cached for a set duration (e.g., 10 minutes). This helps prevent API rate-limiting.
-   **Prevents Duplicate Replies**: The system checks if a comment has already been liked (`comment.has_liked`) to avoid responding to it again.

## 4. Installation Guide

### Prerequisites
-   A Virtual Private Server (VPS) running Ubuntu 20.04 or later.
-   At least 1 GB of RAM.
-   `git` installed on the server.
-   For Docker installation: `Docker` and `Docker Compose` installed.
-   For venv installation: `Python 3.9` or higher installed.

### Installation with Docker (Recommended)
This is the simplest and most stable method for running the application.

**Step 1: Clone the Project**
First, log into your server and run the following command to get the project source code:
```bash
git clone https://github.com/your-username/instagram-automation.git
cd instagram-automation
```

**Step 2: Run the Installation Script**
Make the installation script executable and run it:
```bash
chmod +x install.sh
./install.sh
```
The script will ask you the following:
1.  `Do you want to set ports manually? (y/n)`:
    -   If you enter `n`, the default ports (`8000` for Backend, `8080` for Frontend) will be used.
    -   If you enter `y`, the script will prompt you to enter the desired ports for the backend and frontend.

After you answer, the script will automatically configure the Docker Compose files, then build and run the containers.

**Step 3: Access the Application**
Once the installation is complete, you can access the web UI at `http://<YOUR_SERVER_IP>:<FRONTEND_PORT>`.

### Installation with Python Virtual Environment (venv)
This method is suitable for users who want more control over the execution environment.

**Step 1: Clone the Project**
```bash
git clone https://github.com/your-username/instagram-automation.git
cd instagram-automation
```

**Step 2: Run the venv Setup Script**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```
Similar to the Docker script, this script will ask about port configuration and then:
-   Create a Python virtual environment in the `.venv` folder.
-   Install the required packages from `requirements.txt`.
-   Run the backend and frontend services in the background.

**Step 3: Access the Application**
Like the Docker method, the application will be available at `http://<YOUR_SERVER_IP>:<FRONTEND_PORT>`.

## 5. Making the Service Persistent (venv only)
If you used the `venv` method, the services will not restart automatically after a server reboot. To make the services persistent, you can use `systemd`.

**Step 1: Create Service Files**
Create two service files, one for the backend and one for the frontend.

**`backend.service` file:**
```bash
sudo nano /etc/systemd/system/insta_backend.service
```
Paste the following content. **Note:** Replace the `WorkingDirectory` and `ExecStart` paths with the actual paths to your project.
```ini
[Unit]
Description=Instagram Automation Backend Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/instagram-automation/backend
ExecStart=/root/instagram-automation/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**`frontend.service` file:**
```bash
sudo nano /etc/systemd/system/insta_frontend.service
```
Paste the following content and adjust the paths for your project.
```ini
[Unit]
Description=Instagram Automation Frontend Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/instagram-automation/frontend
ExecStart=/root/instagram-automation/.venv/bin/python -m http.server 8080
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Step 2: Enable and Start the Services**
Run the following commands to enable and start the services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable insta_backend.service
sudo systemctl start insta_backend.service
sudo systemctl enable insta_frontend.service
sudo systemctl start insta_frontend.service
```
You can check the status of the services using `sudo systemctl status insta_backend.service`.

## 6. Usage Guide (Web UI)
1.  **Login**: On the main page, enter your Instagram account username and password, then click "Login".
2.  **Task Management**: After a successful login, you will be redirected to the task management page.
    -   **Add Task**: To add a new task, fill out the form:
        -   **Post URL**: The full link to the post you want to automate.
        -   **Keywords**: The keywords a comment must contain (separated by commas).
        -   **Reply Message**: The message to be sent in reply to the comment.
        -   **DM Message**: The message to be sent to the user's DMs (optional).
        -   **Must Follow**: If checked, automation will only run for your followers.
    -   **Task List**: Active tasks are displayed in a table. You can delete any task.

## 7. API Documentation
All endpoints are accessible from `http://<YOUR_SERVER_IP>:<BACKEND_PORT>`.

### Login
-   **URL**: `/api/login`
-   **Method**: `POST`
-   **Body**:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
-   **Success Response (200)**:
    ```json
    {
      "message": "Logged in successfully",
      "sessionid": "returned_session_id"
    }
    ```

### Task Management
-   **Get All Tasks**:
    -   **URL**: `/api/tasks`
    -   **Method**: `GET`
-   **Add a Task**:
    -   **URL**: `/api/tasks`
    -   **Method**: `POST`
    -   **Body**:
        ```json
        {
          "post_url": "https://www.instagram.com/p/Cxyz...",
          "keywords": "test,hello",
          "reply_message": "Thanks for your comment!",
          "dm_message": "Hello from automation!",
          "must_follow": true
        }
        ```
-   **Delete a Task**:
    -   **URL**: `/api/tasks/{task_id}`
    -   **Method**: `DELETE`

### Dedicated n8n Endpoint
This endpoint is designed to perform various operations via n8n.

-   **URL**: `/api/n8n/action`
-   **Method**: `POST`
-   **Headers**:
    -   `Authorization`: `Bearer <YOUR_JWT_TOKEN>` (This token is the `sessionid` received from the login endpoint)
-   **Body**:
    ```json
    {
      "action": "action_name",
      "params": { ... }
    }
    ```
-   **Available Actions**:
    1.  `check_follower_status`: Checks if one user follows another.
        -   `params`: `{ "user_to_check": "username1", "user_to_check_against": "username2" }`
    2.  `get_user_posts`: Returns a user's latest posts.
        -   `params`: `{ "username": "target_username", "count": 5 }`
    3.  `send_dm`: Sends a direct message.
        -   `params`: `{ "username": "recipient_username", "message": "Your message here" }`

## 8. Advanced n8n Tutorial
In this scenario, we will build an n8n workflow that automatically responds to users who comment on your latest post with a specific keyword. If needed, it will save their information to a Google Sheet and use an AI service to generate a response.

### The Final Scenario:
1.  The workflow runs every 5 minutes.
2.  It fetches your latest post using the `get_user_posts` endpoint.
3.  It checks the comments on that post.
4.  If a comment contains the keyword `ai` and has not been replied to yet:
    a. It checks if the commenter follows you (`check_follower_status`).
    b. If they follow you, it sends the comment text to a Large Language Model (LLM) to generate a suitable reply.
    c. It posts the generated response as a reply to the comment.
    d. It sends a thank-you message to the user's DMs (`send_dm`).
    e. It saves the username and comment text to a Google Sheet.

### Implementation Steps in n8n

**(Screenshots and more specific details will be visible in the n8n UI)**

**Node 1: Schedule Trigger**
-   Set this node to trigger the workflow every 5 minutes.

**Node 2: HTTP Request - Get Last Post**
-   **URL**: `http://<YOUR_SERVER_IP>:<BACKEND_PORT>/api/n8n/action`
-   **Method**: `POST`
-   **Authentication**: `Header Auth`
    -   **Name**: `Authorization`
    -   **Value**: `Bearer {{ $credentials.apiToken.token }}` (Store your token in Credentials)
-   **Body**:
    ```json
    {
      "action": "get_user_posts",
      "params": {
        "username": "your_instagram_username",
        "count": 1
      }
    }
    ```

**Node 3: Loop Over Comments**
-   Use a `Split in Batches` node or similar to process each comment received from the previous node individually.

**Node 4: IF Node - Check for Keyword and Replied Status**
-   Condition 1: `{{ $json.text }}` -> `contains` -> `ai`
-   Condition 2: `{{ $json.has_replied }}` -> `is` -> `false`

**Node 5: HTTP Request - Check Follower Status**
-   (Connected to the `true` output of the IF node)
-   **URL**: `http://.../api/n8n/action`
-   **Method**: `POST`
-   **Body**:
    ```json
    {
      "action": "check_follower_status",
      "params": {
        "user_to_check": "{{ $json.owner.username }}",
        "user_to_check_against": "your_instagram_username"
      }
    }
    ```

**Node 6: IF Node - Is a Follower?**
-   Condition: `{{ $json.is_follower }}` -> `is` -> `true`

**Node 7: AI Agent / LLM Node**
-   (Connected to the `true` output of the previous node)
-   Use the OpenAI node or any other service.
-   **Prompt**: `Generate a friendly and helpful reply to this Instagram comment: "{{ $json.text }}"`

**Node 8: HTTP Request - Reply to Comment**
-   (This would use a `comment_reply` action, which should be added to the project or called via a custom action).
-   **URL**: `http://.../api/n8n/action`
-   **Body**:
    ```json
    {
      "action": "reply_to_comment",
      "params": {
        "comment_id": "{{ $json.pk }}",
        "message": "{{ $node['AI Agent'].json.response }}"
      }
    }
    ```

**Node 9: HTTP Request - Send DM**
-   **URL**: `http://.../api/n8n/action`
-   **Body**:
    ```json
    {
      "action": "send_dm",
      "params": {
        "username": "{{ $json.owner.username }}",
        "message": "Thanks for your great comment! I've replied to it."
      }
    }
    ```

**Node 10: Google Sheets Node**
-   Save the user's info (`username`, `comment text`) to a new sheet.

This workflow is a powerful example of how to combine this tool with n8n to create smart and complex automations.

## 9. Frequently Asked Questions (FAQ)
**Q: Is it safe to use this tool?**
A: Yes. By using random delays and caching mechanisms, we've tried to make the application's behavior as human-like as possible. However, there is always a small risk when using automation tools. It is recommended to use this tool with caution.

**Q: Why does the application sometimes delay replying to comments?**
A: This is part of the application's safety design. Variable intervals between checks make your activity less likely to be flagged as a bot.

**Q: Can I install this tool on Windows?**
A: Yes, it is possible by installing Python and following the venv guide. However, for stable execution, a Linux server with Docker is recommended.

## 10. Project Structure
```
/
├── backend/
│   ├── main.py         # FastAPI application
│   ├── logic.py        # Core automation logic
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env.template       # Environment variables template
├── docker-compose.yml
├── install.sh          # Docker installation script
└── setup_venv.sh       # venv installation script
```
