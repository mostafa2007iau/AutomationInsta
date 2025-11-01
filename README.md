# Instagram Automation Tool

An open-source, self-hosted Instagram automation tool similar to ManyChat, designed to run without official API keys. It provides a backend API and a simple frontend interface to manage comment and DM automation tasks.

This project uses `instagrapi` for Instagram communication and can be deployed easily using Docker.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Docker (Recommended)](#docker-recommended)
  - [Manual Setup (venv)](#manual-setup-venv)
- [How to Use](#how-to-use)
  - [1. Logging In](#1-logging-in)
  - [2. Creating an Automation Task](#2-creating-an-automation-task)
  - [3. Managing Tasks](#3-managing-tasks)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Automation Management](#automation-management)
  - [n8n Integration](#n8n-integration)
- [Connecting with n8n](#connecting-with-n8n)
  - [Example Workflow: Replying to comments with AI](#example-workflow-replying-to-comments-with-ai)
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
- **n8n Integration**: A dedicated endpoint to connect with automation platforms like n8n.

## How It Works

The application consists of two main parts:

1.  **Backend (FastAPI)**: A Python server that handles all the logic. It uses the `instagrapi` library to connect to Instagram, listen for comments on specific posts, and perform actions like replying or sending DMs.
2.  **Frontend (Vanilla JS/HTML/CSS)**: A simple user interface that runs in your browser. It communicates with the backend's API to allow you to log in, create, and manage automation tasks.

When you start an automation task, the backend runs a loop in the background that periodically fetches new comments for the specified post and processes them according to your rules.

## Installation

### Docker (Recommended)

This is the easiest way to get the application running.

**Prerequisites**:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

**Steps**:

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Run the interactive setup script**:
    This script will help you create a `.env` file to configure the application's ports.
    ```bash
    ./install.sh
    ```
    You can choose the default ports (Backend: 8000, Frontend: 8080) or set your own.

3.  **Build and run the containers**:
    ```bash
    docker-compose up --build -d
    ```
    The `-d` flag runs the containers in detached mode (in the background).

4.  **Access the application**:
    -   **Frontend**: Open your browser and go to `http://localhost:<FRONTEND_PORT>` (e.g., `http://localhost:8080`).
    -   **API Docs**: You can explore the API documentation at `http://localhost:<BACKEND_PORT>/docs` (e.g., `http://localhost:8000/docs`).

To stop the application, run `docker-compose down`.

### Manual Setup (venv)

If you prefer not to use Docker, you can run the backend and frontend separately.

**Prerequisites**:
- Python 3.9+
- A simple web server for the frontend (e.g., Python's built-in `http.server`).

**Steps**:

1.  **Clone the repository**.

2.  **Run the venv setup script**:
    This script creates a virtual environment and installs all the required Python packages.
    ```bash
    ./setup_venv.sh
    ```

3.  **Activate the virtual environment**:
    ```bash
    source backend/.venv/bin/activate
    ```

4.  **Run the backend server**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir backend
    ```
    The backend is now running on `http://localhost:8000`.

5.  **Run the frontend server**:
    Open a **new terminal** and run a simple web server from the `frontend` directory.
    ```bash
    python3 -m http.server 8080 --directory frontend
    ```
    The frontend is now accessible at `http://localhost:8080`.

    **Note**: If you change the backend port, remember to update the `API_BASE_URL` constant in `frontend/script.js`.

## How to Use

### 1. Logging In

You have two options to log in to your Instagram account:

-   **Credentials**: Enter your Instagram username and password. The application will log in and create a session file (`<username>_session.json`) to make future logins faster.
-   **Session JSON**: If you already have session data from `instagrapi` or another tool, you can paste the JSON content into the textarea. This is a more secure method as it doesn't require storing your password.

### 2. Creating an Automation Task

Once logged in, you can create a new automation task:

-   **Instagram Post URL**: The full URL of the post you want to monitor.
-   **Keywords**: A comma-separated list of words. The automation will trigger if a comment contains any of these keywords (e.g., `price, info, buy`).
-   **Comment Replies**: A list of replies, one per line. A random reply will be chosen to respond to the triggering comment.
-   **Direct Message Replies**: A list of DMs, one per line. A random DM will be sent to the user who wrote the comment.
-   **Respond to followers only**: If checked, the automation will only respond to users who follow your account.
-   **Message for non-followers**: If the above option is checked, this message will be sent to non-followers instead of the main reply.

### 3. Managing Tasks

The "Active Automations" list shows all the tasks currently running. You can see the post URL and keywords for each task. Click the **Delete** button to stop and remove a task.

## API Documentation

The API is documented with Swagger UI, available at `/docs`.

### Authentication

-   `POST /login/credentials`: Login with username and password.
-   `POST /login/session`: Login with session JSON.
-   `POST /logout`: Logout from the current session.
-   `GET /status`: Check login status.

### Automation Management

-   `POST /automations`: Create a new automation task.
-   `GET /automations`: Get a list of active tasks.
-   `DELETE /automations/{task_id}`: Stop a specific task.

### n8n Integration

-   `POST /api/n8n/action`: A generic endpoint for n8n.

    **Body format**:
    ```json
    {
      "action": "action_name",
      "payload": { ... }
    }
    ```

    **Supported Actions**:
    1.  **`send_dm`**:
        -   **Payload**: `{ "user_id": "12345", "text": "Hello!" }`
    2.  **`post_comment`**:
        -   **Payload**: `{ "media_id": "12345", "text": "Great post!" }`
    3.  **`get_media_comments`**:
        -   **Payload**: `{ "media_id": "12345", "amount": 30 }`

---

# Farsi Documentation (مستندات فارسی)

یک ابزار اتوماسیون اینستاگرام متن-باز و سلف-هاست (قابل میزبانی روی سرور شخصی) که مشابه ManyChat عمل می‌کند، با این تفاوت که نیازی به کلید API رسمی اینستاگرام ندارد. این پروژه یک API در Backend و یک رابط کاربری ساده در Frontend برای مدیریت تسک‌های اتوماسیون کامنت و دایرکت فراهم می‌کند.

این پروژه از کتابخانه `instagrapi` برای ارتباط با اینستاگرام استفاده کرده و به راحتی با استفاده از Docker قابل راه‌اندازی است.

---

## فهرست مطالب

- [قابلیت‌ها](#قابلیت‌ها)
- [شیوه عملکرد](#شیوه-عملکرد)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
  - [روش اول: Docker (توصیه شده)](#روش-اول-docker-توصیه-شده)
  - [روش دوم: نصب دستی (venv)](#روش-دوم-نصب-دستی-venv)
- [راهنمای استفاده](#راهنمای-استفاده)
  - [۱. ورود به حساب کاربری](#۱-ورود-به-حساب-کاربری)
  - [۲. ساخت تسک اتومیشن](#۲-ساخت-تسک-اتومیشن)
  - [۳. مدیریت تسک‌ها](#۳-مدیریت-تسک‌ها)
- [مستندات API](#مستندات-api)
  - [احراز هویت (Authentication)](#احراز-هویت-authentication)
  - [مدیریت اتومیشن (Automation Management)](#مدیریت-اتومیشن-automation-management)
  - [اتصال به n8n (n8n Integration)](#اتصال-به-n8n-n8n-integration)
- [آموزش اتصال به n8n](#آموزش-اتصال-به-n8n)
  - [مثال: پاسخ به کامنت‌ها با هوش مصنوعی](#مثال-پاسخ-به-کامنت‌ها-با-هوش-مصنوعی)

---

## قابلیت‌ها

- **اتوماسیون دایرکت و کامنت**: پاسخ خودکار به کامنت‌ها و ارسال دایرکت بر اساس کلمات کلیدی.
- **حالت فقط فالوورها**: محدود کردن اتومیشن فقط به کاربرانی که پیج را فالو کرده‌اند.
- **پاسخ‌های سفارشی**: امکان تنظیم چندین پاسخ مختلف که به صورت رندوم برای کامنت و دایرکت انتخاب شوند.
- **بدون نیاز به API رسمی**: استفاده از API خصوصی اینستاگرام از طریق `instagrapi`.
- **رابط کاربری ساده**: یک پنل تحت وب برای مدیریت آسان تسک‌های اتومیشن.
- **نصب آسان با Docker**: راه‌اندازی سریع و بی‌دردسر با Docker و Docker Compose.
- **اتصال به n8n**: یک Endpoint اختصاصی برای اتصال به پلتفرم‌های اتومیشن مانند n8n.

## شیوه عملکرد

این اپلیکیشن از دو بخش اصلی تشکیل شده است:

1.  **Backend (FastAPI)**: یک سرور پایتون که تمام منطق اصلی را مدیریت می‌کند. این بخش با استفاده از کتابخانه `instagrapi` به اینستاگرام متصل شده، کامنت‌های پست‌های مشخص شده را مانیتور کرده و اقداماتی مانند پاسخ یا ارسال دایرکت را انجام می‌دهد.
2.  **Frontend (Vanilla JS/HTML/CSS)**: یک رابط کاربری ساده که در مرورگر شما اجرا می‌شود و با API بک‌اند ارتباط برقرار می‌کند تا به شما اجازه دهد وارد حساب خود شده، تسک‌های اتومیشن را ساخته و مدیریت کنید.

وقتی شما یک تسک اتومیشن را شروع می‌کنید، بک‌اند یک حلقه (loop) در پس‌زمینه اجرا می‌کند که به صورت دوره‌ای کامنت‌های جدید پست مورد نظر را دریافت و طبق قوانین تعریف شده توسط شما، آن‌ها را پردازش می‌کند.

## نصب و راه‌اندازی

### روش اول: Docker (توصیه شده)

این ساده‌ترین روش برای راه‌اندازی اپلیکیشن است.

**پیش‌نیازها**:
- [نرم‌افزار Docker](https://www.docker.com/get-started)
- [نرم‌افزار Docker Compose](https://docs.docker.com/compose/install/)

**مراحل**:

۱. **دریافت پروژه**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

۲. **اجرای اسکریپت نصب**:
   این اسکریپت به شما کمک می‌کند تا فایل `.env` را برای تنظیم پورت‌های اپلیکیشن بسازید.
   ```bash
   ./install.sh
   ```
   شما می‌توانید پورت‌های پیش‌فرض (بک‌اند: 8000، فرانت‌اند: 8080) را انتخاب کرده یا مقادیر دلخواه خود را وارد کنید.

۳. **ساخت و اجرای کانتینرها**:
   ```bash
   docker-compose up --build -d
   ```
   فلگ `-d` باعث می‌شود کانتینرها در پس‌زمینه اجرا شوند.

۴. **دسترسی به اپلیکیشن**:
   -   **رابط کاربری (Frontend)**: مرورگر خود را باز کرده و به آدرس `http://localhost:<FRONTEND_PORT>` (مثلاً `http://localhost:8080`) بروید.
   -   **مستندات API**: مستندات کامل API در آدرس `http://localhost:<BACKEND_PORT>/docs` (مثلاً `http://localhost:8000/docs`) در دسترس است.

برای متوقف کردن اپلیکیشن، دستور `docker-compose down` را اجرا کنید.

### روش دوم: نصب دستی (venv)

اگر تمایلی به استفاده از Docker ندارید، می‌توانید بک‌اند و فرانت‌اند را به صورت جداگانه اجرا کنید.

**پیش‌نیازها**:
- پایتون نسخه 3.9 یا بالاتر
- یک وب سرور ساده برای فرانت‌اند (مانند `http.server` خود پایتون).

**مراحل**:

۱. **پروژه را دریافت کنید**.

۲. **اسکریپت نصب venv را اجرا کنید**:
   این اسکریپت یک محیط مجازی پایتون ساخته و تمام پکیج‌های مورد نیاز را نصب می‌کند.
   ```bash
   ./setup_venv.sh
   ```

۳. **محیط مجازی را فعال کنید**:
   ```bash
   source backend/.venv/bin/activate
   ```

۴. **سرور بک‌اند را اجرا کنید**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir backend
   ```
   بک‌اند اکنون روی آدرس `http://localhost:8000` در حال اجراست.

۵. **سرور فرانت‌اند را اجرا کنید**:
   یک **ترمینال جدید** باز کرده و یک وب سرور ساده را از پوشه `frontend` اجرا کنید.
   ```bash
   python3 -m http.server 8080 --directory frontend
   ```
   فرانت‌اند اکنون روی آدرس `http://localhost:8080` در دسترس است.

   **نکته**: اگر پورت بک‌اند را تغییر دادید، حتماً مقدار ثابت `API_BASE_URL` را در فایل `frontend/script.js` به‌روزرسانی کنید.

## راهنمای استفاده

### ۱. ورود به حساب کاربری

شما دو راه برای ورود به حساب اینستاگرام خود دارید:

-   **نام کاربری و رمز عبور**: با وارد کردن اطلاعات حساب خود، اپلیکیشن وارد شده و یک فایل نشست (`<username>_session.json`) ایجاد می‌کند تا ورودهای بعدی سریع‌تر انجام شود.
-   **Session JSON**: اگر از قبل اطلاعات نشست (Session) را از `instagrapi` یا ابزار دیگری در اختیار دارید، می‌توانید محتوای JSON آن را در فیلد مربوطه وارد کنید. این روش امن‌تر است زیرا نیازی به ذخیره رمز عبور شما ندارد.

### ۲. ساخت تسک اتومیشن

پس از ورود، می‌توانید یک تسک اتومیشن جدید بسازید:

-   **آدرس پست اینستاگرام**: آدرس کامل پستی که می‌خواهید کامنت‌های آن مانیتور شود.
-   **کلمات کلیدی**: لیستی از کلمات که با کاما (`,`) از هم جدا شده‌اند. اگر کامنتی حاوی یکی از این کلمات باشد، اتومیشن فعال می‌شود (مثال: `قیمت, سفارش, خرید`).
-   **پاسخ‌های کامنت**: لیستی از پاسخ‌ها که هر کدام در یک خط جداگانه نوشته شده‌اند. یک پاسخ به صورت رندوم برای کامنت ارسال می‌شود.
-   **پاسخ‌های دایرکت**: لیستی از پیام‌های دایرکت که هر کدام در یک خط جداگانه نوشته شده‌اند. یک پیام به صورت رندوم برای کاربر ارسال می‌شود.
-   **فقط به فالوورها پاسخ بده**: اگر این گزینه فعال باشد، اتومیشن فقط برای کاربرانی که شما را فالو کرده‌اند اجرا می‌شود.
-   **پیام برای غیرفالوورها**: اگر گزینه بالا فعال باشد، این پیام به جای پاسخ اصلی برای کاربرانی که شما را فالو نکرده‌اند ارسال می‌شود.

### ۳. مدیریت تسک‌ها

در بخش "Active Automations" می‌توانید لیست تسک‌های در حال اجرا را مشاهده کنید. با کلیک روی دکمه **Delete** می‌توانید یک تسک را متوقف و حذف کنید.

## مستندات API

مستندات کامل و تعاملی API با Swagger UI در آدرس `/docs` سرور بک‌اند موجود است.

### احراز هویت (Authentication)

-   `POST /login/credentials`: ورود با نام کاربری و رمز عبور.
-   `POST /login/session`: ورود با اطلاعات نشست (Session JSON).
-   `POST /logout`: خروج از حساب کاربری.
-   `GET /status`: بررسی وضعیت ورود.

### مدیریت اتومیشن (Automation Management)

-   `POST /automations`: ساخت یک تسک اتومیشن جدید.
-   `GET /automations`: دریافت لیست تسک‌های فعال.
-   `DELETE /automations/{task_id}`: متوقف کردن یک تسک مشخص.

### اتصال به n8n (n8n Integration)

-   `POST /api/n8n/action`: یک Endpoint عمومی برای n8n.

    **فرمت Body**:
    ```json
    {
      "action": "نام_عملیات",
      "payload": { ... }
    }
    ```

    **عملیات‌های پشتیبانی شده**:
    1.  **`send_dm`**: ارسال دایرکت.
        -   **Payload**: `{ "user_id": "12345", "text": "سلام!" }`
    2.  **`post_comment`**: ثبت کامنت.
        -   **Payload**: `{ "media_id": "12345", "text": "پست عالی بود!" }`
    3.  **`get_media_comments`**: دریافت کامنت‌های یک پست.
        -   **Payload**: `{ "media_id": "12345", "amount": 30 }`


## آموزش اتصال به n8n

شما می‌توانید از Endpoint اختصاصی n8n برای ساخت ورک‌فلوهای قدرتمند استفاده کنید.

### مثال: پاسخ به کامنت‌ها با هوش مصنوعی

در این سناریو، ما یک ورک‌فلو در n8n می‌سازیم که:
۱. هر چند دقیقه یک‌بار، کامنت‌های جدید یک پست را از اپلیکیشن ما دریافت می‌کند.
۲. متن کامنت‌ها را به یک سرویس هوش مصنوعی (مانند OpenAI) ارسال می‌کند تا یک پاسخ هوشمند تولید شود.
۳. پاسخ تولید شده را با استفاده از اپلیکیشن ما زیر همان کامنت ارسال می‌کند.

**مراحل ساخت ورک‌فلو در n8n**:

1.  **نود شروع (Cron Node)**:
    -   یک نود **Cron** اضافه کنید و آن را تنظیم کنید تا هر ۵ دقیقه یک‌بار اجرا شود (`*/5 * * * *`).

2.  **نود HTTP Request (برای دریافت کامنت‌ها)**:
    -   یک نود **HTTP Request** اضافه کنید و تنظیمات زیر را وارد نمایید:
        -   **Method**: `POST`
        -   **URL**: `http://<YOUR_BACKEND_HOST>:<PORT>/api/n8n/action`
        -   **Body Content Type**: `JSON`
        -   **Body**:
            ```json
            {
              "action": "get_media_comments",
              "payload": {
                "media_id": "YOUR_INSTAGRAM_MEDIA_ID"
              }
            }
            ```
            > **نکته**: `media_id` همان `pk` پست است که می‌توانید از طریق ابزارهای دیگر یا API خود اینستاگرام به دست آورید.

3.  **نود SplitInBatches (برای پردازش تک‌تک کامنت‌ها)**:
    -   یک نود **SplitInBatches** اضافه کنید و `Field to Split` را روی `data` تنظیم کنید. این کار باعث می‌شود هر کامنت به صورت یک آیتم جداگانه در n8n پردازش شود.

4.  **نود AI (مانند OpenAI)**:
    -   یک نود **OpenAI** یا هر سرویس AI دیگری اضافه کنید.
    -   در قسمت **Prompt**، از n8n بخواهید تا یک پاسخ برای متن کامنت دریافتی از مرحله قبل تولید کند. مثال:
        `Based on this comment: "{{$json["text"]}}", write a friendly and helpful reply.`

5.  **نود HTTP Request (برای ارسال پاسخ)**:
    -   یک نود **HTTP Request** دیگر اضافه کنید:
        -   **Method**: `POST`
        -   **URL**: `http://<YOUR_BACKEND_HOST>:<PORT>/api/n8n/action`
        -   **Body Content Type**: `JSON`
        -   **Body**:
            ```json
            {
              "action": "post_comment",
              "payload": {
                "media_id": "{{$json["media"]["pk"]}}",
                "text": "{{$json["choices"][0]["message"]["content"]}}"
              }
            }
            ```
            > **توضیح**: در اینجا ما `media_id` را از داده‌های کامنت اصلی و `text` را از خروجی نود OpenAI دریافت می‌کنیم.

با فعال کردن این ورک‌فلو، شما یک سیستم پاسخ‌دهی هوشمند به کامنت‌ها خواهید داشت که به صورت خودکار کار می‌کند.
