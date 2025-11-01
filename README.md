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
  - [Workflow 1: Login to Instagram (Run Once)](#workflow-1-login-to-instagram-run-once)
  - [Workflow 2: AI-Powered Comment Replies (Scheduled)](#workflow-2-ai-powered-comment-replies-scheduled)
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

## Connecting with n8n

You can use the dedicated n8n endpoint (`/api/n8n/action`) to build powerful, custom automation workflows. Below are two essential workflows to get you started.

### Workflow 1: Login to Instagram (Run Once)

Before running any other workflows, you must log in to your Instagram account via the API. This workflow only needs to be run **once** successfully. The application will maintain the session for future actions.

**Choose one of the two methods below.**

#### Method A: Login with Credentials

```
+----------------------------------------------+
| [1] Manual Start                             |
|     (Executes the workflow once)             |
+----------------------------------------------+
                  |
                  |
                  v
+----------------------------------------------+
| [2] Login with Credentials (HTTP Request)    |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/login/credentials |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "username": "your_instagram_username",   |
|     "password": "your_instagram_password"    |
|   }                                          |
+----------------------------------------------+
```

#### Method B: Login with Session JSON

This is the recommended method if you have your session data.

```
+----------------------------------------------+
| [1] Manual Start                             |
|     (Executes the workflow once)             |
+----------------------------------------------+
                  |
                  |
                  v
+----------------------------------------------+
| [2] Login with Session (HTTP Request)        |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/login/session |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "session_data": {                        |
|       "sessionid": "...",                    |
|       "csrftoken": "...",                    |
|       "...": "..."                           |
|     }                                        |
|   }                                          |
+----------------------------------------------+
```

After executing either of these workflows, the backend will be logged in and ready to handle automation tasks.

### Workflow 2: AI-Powered Comment Replies (Scheduled)

This workflow runs on a schedule, fetches new comments from a specific post, uses an AI agent to generate intelligent replies, and posts them back to Instagram.

#### Overall Workflow Diagram

```
+--------------+   +-------------------+   +-----------------+   +------------------+   +--------------------+
| [1] Cron     |-->| [2] Get Comments  |-->| [3] Split Items |-->| [4] AI Agent     |-->| [5] Post Reply     |
| (Every 5m)   |   | (HTTP Request)    |   | (SplitInBatches)|   | (e.g., OpenAI)   |   | (HTTP Request)     |
+--------------+   +-------------------+   +-----------------+   +------------------+   +--------------------+
```

#### Step-by-Step Node Configuration

**Step 1: Cron Node (Trigger)**
This node starts the workflow on a schedule.

```
+----------------------------------------------+
| [1] Cron (Schedule Trigger)                  |
+----------------------------------------------+
| Mode:           Every X Minutes              |
| Minutes:        5                            |
+----------------------------------------------+
```

**Step 2: Get Comments Node (HTTP Request)**
This node calls our API to fetch the latest comments for a specific post.

```
+----------------------------------------------+
| [2] Get Comments (HTTP Request)              |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/api/n8n/action |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "action": "get_media_comments",           |
|     "payload": {                             |
|       "media_id": "YOUR_POST_MEDIA_ID"       |
|     }                                        |
|   }                                          |
| Options:                                     |
|   Split Into:   Items                        |
|   Path:         data                         |
+----------------------------------------------+
```
> **Note**: `media_id` is the unique identifier for an Instagram post (e.g., `319_12345...`). You can find this using various online tools or from the post's URL structure. The `Split Into: Items` option automatically processes each comment individually in the next steps.

**Step 3: AI Agent Node (e.g., OpenAI)**
This node receives the comment text and generates a human-like reply.

```
+----------------------------------------------+
| [4] OpenAI (AI Agent)                        |
+----------------------------------------------+
| Resource:       Chat                         |
| Model:          gpt-4o                       |
| Prompt:                                      |
|   Based on this Instagram comment:           |
|   "{{ $json.text }}"                         |
|                                              |
|   Write a friendly and engaging reply.       |
|   Keep it concise and positive.              |
|                                              |
+----------------------------------------------+
```
> The `{{ $json.text }}` expression dynamically inserts the text from the comment received in the previous step.

**Step 4: Post Reply Node (HTTP Request)**
This final node sends the AI-generated reply back to our API to be posted on Instagram.

```
+----------------------------------------------+
| [5] Post Reply (HTTP Request)                |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/api/n8n/action |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "action": "post_comment",                 |
|     "payload": {                             |
|       "media_id": "{{ $json.media.pk }}",    |
|       "text": "{{ $('OpenAI').json.choices[0].message.content }}" |
|     }                                        |
|   }                                          |
+----------------------------------------------+
```
> **Expressions Explained**:
> - `{{ $json.media.pk }}`: This retrieves the `pk` (same as `media_id`) of the post from the original comment data.
> - `{{ $('OpenAI').json.choices[0].message.content }}`: This retrieves the generated text content from the output of the OpenAI node.

By setting up this workflow, you create a fully automated and intelligent comment management system.

---
- [Project Structure](#project-structure)
- [Farsi Documentation (مستندات فارسی)](#farsi-documentation-مستندات-فارسی)

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
  - [ورک‌فلو ۱: لاگین به اینستاگرام (فقط یک بار اجرا شود)](#ورک‌فلو-۱-لاگین-به-اینستاگرام-فقط-یک-بار-اجرا-شود)
  - [ورک‌فلو ۲: پاسخ هوشمند به کامنت‌ها با AI (زمان‌بندی شده)](#ورک‌فلو-۲-پاسخ-هوشمند-به-کامنت‌ها-با-ai-زمان‌بندی-شده)

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

شما می‌توانید از Endpoint اختصاصی n8n برای ساخت ورک‌فلوهای قدرتمند و سفارشی استفاده کنید. در ادامه دو ورک‌فلو ضروری برای شروع کار شما توضیح داده شده است.

### ورک‌فلو ۱: لاگین به اینستاگرام (فقط یک بار اجرا شود)

قبل از اجرای هر ورک‌فلو دیگری، باید از طریق API به حساب اینستاگرام خود لاگین کنید. این ورک‌فلو فقط **یک بار** نیاز به اجرای موفقیت‌آمیز دارد. اپلیکیشن، نشست (Session) را برای اقدامات بعدی فعال نگه می‌دارد.

**یکی از دو روش زیر را انتخاب کنید.**

#### روش الف: ورود با نام کاربری و رمز عبور

```
+----------------------------------------------+
| [1] Start (شروع دستی)                        |
|     (ورک‌فلو را یک بار اجرا می‌کند)             |
+----------------------------------------------+
                  |
                  |
                  v
+----------------------------------------------+
| [2] Login with Credentials (HTTP Request)    |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/login/credentials |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "username": "your_instagram_username",   |
|     "password": "your_instagram_password"    |
|   }                                          |
+----------------------------------------------+
```

#### روش ب: ورود با Session JSON

این روش در صورتی که اطلاعات نشست (Session) خود را داشته باشید، توصیه می‌شود.

```
+----------------------------------------------+
| [1] Start (شروع دستی)                        |
|     (ورک‌فلو را یک بار اجرا می‌کند)             |
+----------------------------------------------+
                  |
                  |
                  v
+----------------------------------------------+
| [2] Login with Session (HTTP Request)        |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/login/session |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "session_data": {                        |
|       "sessionid": "...",                    |
|       "csrftoken": "...",                    |
|       "...": "..."                           |
|     }                                        |
|   }                                          |
+----------------------------------------------+
```

پس از اجرای موفقیت‌آمیز یکی از این دو ورک‌فلو، بک‌اند به حساب شما متصل شده و آماده اجرای تسک‌های اتوماسیون است.

### ورک‌فلو ۲: پاسخ هوشمند به کامنت‌ها با AI (زمان‌بندی شده)

این ورک‌فلو به صورت زمان‌بندی شده اجرا می‌شود، کامنت‌های جدید یک پست مشخص را دریافت می‌کند، از یک عامل هوش مصنوعی برای تولید پاسخ‌های هوشمند استفاده می‌کند و آن‌ها را در اینستاگرام منتشر می‌کند.

#### دیاگرام کلی ورک‌فلو

```
+--------------+   +-------------------+   +-----------------+   +------------------+   +--------------------+
| [1] Cron     |-->| [2] دریافت کامنت‌ها |-->| [3] تفکیک آیتم‌ها |-->| [4] عامل AI      |-->| [5] ارسال پاسخ      |
| (هر ۵ دقیقه)  |   | (HTTP Request)    |   | (SplitInBatches)|   | (مثلاً OpenAI)   |   | (HTTP Request)     |
+--------------+   +-------------------+   +-----------------+   +------------------+   +--------------------+
```

#### تنظیمات قدم به قدم نودها

**قدم ۱: نود Cron (شروع‌کننده)**
این نود ورک‌فلو را بر اساس یک زمان‌بندی مشخص شروع می‌کند.

```
+----------------------------------------------+
| [1] Cron (شروع زمان‌بندی شده)                |
+----------------------------------------------+
| Mode:           Every X Minutes              |
| Minutes:        5                            |
+----------------------------------------------+
```

**قدم ۲: نود دریافت کامنت‌ها (HTTP Request)**
این نود با API ما ارتباط برقرار کرده و آخرین کامنت‌های یک پست مشخص را دریافت می‌کند.

```
+----------------------------------------------+
| [2] Get Comments (HTTP Request)              |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/api/n8n/action |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "action": "get_media_comments",           |
|     "payload": {                             |
|       "media_id": "YOUR_POST_MEDIA_ID"       |
|     }                                        |
|   }                                          |
| Options:                                     |
|   Split Into:   Items                        |
|   Path:         data                         |
+----------------------------------------------+
```
> **نکته**: `media_id` شناسه‌ی یکتای یک پست در اینستاگرام است (مثلاً `319_12345...`). شما می‌توانید این شناسه را با ابزارهای آنلاین مختلف یا از ساختار URL پست پیدا کنید. گزینه `Split Into: Items` باعث می‌شود هر کامنت به صورت مجزا در مراحل بعدی پردازش شود.

**قدم ۳: نود عامل هوش مصنوعی (مثلاً OpenAI)**
این نود متن کامنت را دریافت کرده و یک پاسخ انسان-مانند تولید می‌کند.

```
+----------------------------------------------+
| [4] OpenAI (عامل هوش مصنوعی)                 |
+----------------------------------------------+
| Resource:       Chat                         |
| Model:          gpt-4o                       |
| Prompt:                                      |
|   Based on this Instagram comment:           |
|   "{{ $json.text }}"                         |
|                                              |
|   Write a friendly and engaging reply in Persian. |
|   Keep it concise and positive.              |
|                                              |
+----------------------------------------------+
```
> عبارت `{{ $json.text }}` متن کامنت دریافت شده از مرحله قبل را به صورت پویا در پرامپت قرار می‌دهد.

**قدم ۴: نود ارسال پاسخ (HTTP Request)**
این نود نهایی، پاسخ تولید شده توسط AI را به API ما ارسال می‌کند تا در اینستاگرام منتشر شود.

```
+----------------------------------------------+
| [5] Post Reply (HTTP Request)                |
+----------------------------------------------+
| Method:         POST                         |
| URL:            http://localhost:8000/api/n8n/action |
| Body Type:      JSON                         |
| Body:                                        |
|   {                                          |
|     "action": "post_comment",                 |
|     "payload": {                             |
|       "media_id": "{{ $json.media.pk }}",    |
|       "text": "{{ $('OpenAI').json.choices[0].message.content }}" |
|     }                                        |
|   }                                          |
+----------------------------------------------+
```
> **توضیح عبارات**:
> - `{{ $json.media.pk }}`: این عبارت `pk` (معادل `media_id`) پست را از داده‌های اصلی کامنت بازیابی می‌کند.
> - `{{ $('OpenAI').json.choices[0].message.content }}`: این عبارت، متن تولید شده توسط نود OpenAI را از خروجی آن استخراج می‌کند.

با راه‌اندازی این ورک‌فلو، شما یک سیستم مدیریت کامنت تماماً خودکار و هوشمند خواهید داشت.
