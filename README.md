# Instagram Automation Tool

This document provides a comprehensive, beginner-friendly guide to the Instagram Automation Tool, covering its features, installation, usage, and advanced integration with n8n via webhooks.

---

<details>
<summary>🇮🇷 **فهرست مطالب (برای باز شدن کلیک کنید)**</summary>

1.  [معرفی پروژه](#معرفی-پروژه-fa)
2.  [قابلیت‌های کلیدی](#قابلیت-های-کلیدی-fa)
3.  [راهنمای نصب (Docker)](#راهنمای-نصب-docker-fa)
4.  [راهنمای استفاده](#راهنمای-استفاده-fa)
5.  [آموزش اتصال به n8n (با Webhook)](#آموزش-اتصال-به-n8n-با-webhook-fa)
    *   [چرا Webhook؟](#چرا-webhook-fa)
    *   [سناریوی گردش کار](#سناریوی-گردش-کار-fa)
    *   [مراحل پیاده‌سازی در n8n](#مراحل-پیاده-سازی-در-n8n-fa)
6.  [مستندات API](#مستندات-api-fa)

</details>

<details>
<summary>🇬🇧 **Table of Contents (Click to expand)**</summary>

1.  [Introduction](#introduction-en)
2.  [Core Features](#core-features-en)
3.  [Installation Guide (Docker)](#installation-guide-docker-en)
4.  [Usage Guide](#usage-guide-en)
5.  [n8n Integration Tutorial (with Webhooks)](#n8n-integration-tutorial-with-webhooks-en)
    *   [Why Webhooks?](#why-webhooks-en)
    *   [Workflow Scenario](#workflow-scenario-en)
    *   [Implementation Steps in n8n](#implementation-steps-in-n8n-en)
6.  [API Documentation](#api-documentation-en)

</details>

---

# 🇮🇷 مستندات فارسی (Farsi Documentation) {#معرفی-پروژه-fa}

## ۱. معرفی پروژه
این پروژه یک ابزار اتوماسیون اینستاگرام است که به شما اجازه می‌دهد وظایف تکراری مانند پاسخ به کامنت‌ها و ارسال دایرکت را به صورت خودکار انجام دهید. این ابزار با تمرکز بر سادگی، ایمنی و قابلیت ادغام با پلتفرم‌های دیگر مانند n8n ساخته شده است.

## ۲. قابلیت‌های کلیدی {#قابلیت-های-کلیدی-fa}
-   **ورود دوگانه**: امکان ورود به حساب کاربری با نام کاربری و رمز عبور یا `sessionid`.
-   **پاسخ‌های تصادفی**: می‌توانید لیستی از پاسخ‌ها را برای کامنت‌ها و دایرکت‌ها تعریف کنید تا ربات در هر بار یک پاسخ تصادفی ارسال کند و طبیعی‌تر به نظر برسد.
-   **یکپارچه‌سازی با n8n از طریق Webhook**: به محض دریافت یک کامنت جدید که با کلمات کلیدی شما مطابقت دارد، برنامه یک نوتیفیکیشن لحظه‌ای به n8n ارسال می‌کند.
-   **رابط کاربری ساده**: یک پنل وب برای مدیریت آسان وظایف، وب‌هوک‌ها و مشاهده وضعیت.
-   **نصب آسان با Docker**: یک اسکریپت نصب خودکار که کل فرآیند را برای شما انجام می‌دهد.

## ۳. راهنمای نصب (Docker) {#راهنمای-نصب-docker-fa}
این پروژه برای اجرا در Docker طراحی شده است. اسکریپت نصب تمام مراحل را به صورت خودکار انجام می‌دهد.

**پیش‌نیازها:**
-   یک سرور (VPS) با سیستم‌عامل Ubuntu 20.04 یا بالاتر.
-   `Docker` و `Docker Compose` نصب شده باشد.
-   دسترسی `sudo`.

**مراحل نصب:**
۱. پروژه را از گیت‌هاب کلون کنید:
```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>
```
۲. اسکریپت نصب را با دسترسی `sudo` اجرا کنید:
```bash
sudo chmod +x install.sh
sudo ./install.sh
```
اسکریپت از شما سوالات زیر را خواهد پرسید:
-   **محل نصب:** می‌توانید پروژه را در مسیر فعلی یا در پوشه‌های سیستمی مانند `/opt` نصب کنید.
-   **پیکربندی پورت:** می‌توانید از پورت پیش‌فرض (8080) استفاده کنید یا یک پورت دلخواه وارد نمایید.

پس از پاسخ به سوالات، اسکریپت به طور خودکار کانتینرها را ساخته و اجرا می‌کند. پس از اتمام، می‌توانید از طریق آدرس `http://<YOUR_SERVER_IP>:<PORT>` به رابط کاربری دسترسی پیدا کنید.

## ۴. راهنمای استفاده {#راهنمای-استفاده-fa}
-   **ورود**: در صفحه اصلی، یکی از دو روش ورود (نام کاربری/رمز عبور یا Session ID) را انتخاب و اطلاعات خود را وارد کنید.
-   **افزودن وظیفه**: در داشبورد، URL پست، کلمات کلیدی و پیام‌های خود را وارد کنید. برای پاسخ‌های چندگانه، هر پاسخ را در یک خط جداگانه بنویسید.
-   **مدیریت Webhook**: در بخش Webhook، آدرس URL گردش کار n8n خود را وارد کنید تا نوتیفیکیشن‌ها به آن ارسال شوند.

## ۵. آموزش اتصال به n8n (با Webhook) {#آموزش-اتصال-به-n8n-با-webhook-fa}

### چرا Webhook؟ {#چرا-webhook-fa}
به جای اینکه n8n هر چند دقیقه یک‌بار از برنامه ما سوال کند که "آیا کامنت جدیدی هست؟"، برنامه ما به محض دریافت کامنت، به n8n خبر می‌دهد. این روش سریع‌تر، بهینه‌تر و آنی است.

### سناریوی گردش کار {#سناریوی-گردش-کار-fa}
می‌خواهیم یک گردش کار بسازیم که:
1.  وقتی کامنتی با کلمه کلیدی شما دریافت می‌شود، فوراً فعال شود.
2.  از یک سرویس هوش مصنوعی (مانند OpenAI) برای تولید یک پاسخ هوشمند به کامنت استفاده کند.
3.  پاسخ تولید شده را به عنوان ریپلای به کامنت اصلی در اینستاگرام ارسال کند.

### مراحل پیاده‌سازی در n8n {#مراحل-پیاده-سازی-در-n8n-fa}

**مرحله ۱: ساخت Webhook Trigger در n8n**
-   یک گردش کار جدید در n8n بسازید.
-   اولین نود را `Webhook` انتخاب کنید.
-   یک URL تست (Test URL) توسط n8n ساخته می‌شود. آن را کپی کنید.

**مرحله ۲: ثبت Webhook در برنامه**
-   به داشبورد برنامه اینستاگرام خود بروید.
-   URL کپی شده از n8n را در بخش "Webhook Management" وارد کرده و اضافه کنید.

**مرحله ۳: ارسال یک نمونه داده به n8n**
-   در اینستاگرام، زیر پستی که برای آن اتوماسیون تعریف کرده‌اید، یک کامنت حاوی کلمه کلیدی خود بنویسید.
-   برنامه ما فوراً اطلاعات کامنت را به n8n ارسال می‌کند و نود Webhook در n8n داده‌ها را دریافت می‌کند.

**مرحله ۴: افزودن نود AI (هوش مصنوعی)**
-   یک نود `OpenAI` (یا هر سرویس دیگری) به گردش کار اضافه کنید.
-   **Prompt**: `Generate a friendly and helpful reply to this Instagram comment: "{{ $json.body.text }}"`

**مرحله ۵: افزودن نود HTTP Request برای ارسال ریپلای**
-   یک نود `HTTP Request` به گردش کار اضافه کنید.
-   **Method**: `POST`
-   **URL**: `http://<YOUR_SERVER_IP>:<PORT>/api/automations/reply`  **(این یک اندپوینت جدید است که باید اضافه شود)**
-   **Authentication**: `Header Auth`.
    -   **Name**: `Authorization`
    -   **Value**: `Bearer {{ $credentials.apiToken.token }}` (توکن شما همان `sessionid` است که پس از ورود دریافت می‌کنید).
-   **Body (JSON)**:
    ```json
    {
      "comment_id": "{{ $json.body.pk }}",
      "reply_text": "{{ $json.choices[0].message.content }}"
    }
    ```
اکنون گردش کار n8n شما آماده است!

## ۶. مستندات API {#مستندات-api-fa}
-   **ورود**: `POST /api/login/credentials`, `POST /api/login/session`
-   **مدیریت وظایف**: `GET /api/automations`, `POST /api/automations`, `DELETE /api/automations/{task_id}`
-   **مدیریت وب‌هوک**: `GET /api/webhooks`, `POST /api/webhooks`, `DELETE /api/webhooks`
-   **ارسال ریپلای**: `POST /api/automations/reply`

---

# 🇬🇧 English Documentation {#introduction-en}

## 1. Introduction
This project is an Instagram automation tool that allows you to automate repetitive tasks like replying to comments and sending DMs. It's built with a focus on simplicity, safety, and integration with platforms like n8n.

## 2. Core Features {#core-features-en}
-   **Dual Login**: Log in with either username/password or a `sessionid`.
-   **Randomized Replies**: Define a list of replies for comments and DMs. The bot will pick one randomly to appear more natural.
-   **Webhook Integration for n8n**: Get instant notifications sent to your n8n workflow as soon as a matching comment is posted.
-   **Simple UI**: A clean web panel to easily manage your tasks, webhooks, and status.
-   **Easy Docker Install**: A fully automated script that handles the entire setup process.

## 3. Installation Guide (Docker) {#installation-guide-docker-en}
This project is designed to run in Docker. The installation script automates all the necessary steps.

**Prerequisites:**
-   A server (VPS) with Ubuntu 20.04 or higher.
-   `Docker` and `Docker Compose` installed.
-   `sudo` access.

**Installation Steps:**
1.  Clone the project from GitHub:
    ```bash
    git clone <REPOSITORY_URL>
    cd <REPOSITORY_FOLDER>
    ```
2.  Run the installation script with `sudo`:
    ```bash
    sudo chmod +x install.sh
    sudo ./install.sh
    ```
The script will ask you:
-   **Installation Path:** You can install in the current directory or a system path like `/opt`.
-   **Port Configuration:** Use the default port (8080) or specify a custom one.

The script will then automatically build and run the Docker containers. Once finished, you can access the UI at `http://<YOUR_SERVER_IP>:<PORT>`.

## 4. Usage Guide {#usage-guide-en}
-   **Login**: On the homepage, choose one of the two login methods.
-   **Add Task**: In the dashboard, enter the post URL, keywords, and your messages. For multiple replies, write each one on a new line.
-   **Manage Webhooks**: In the Webhook section, add your n8n workflow URL to receive notifications.

## 5. n8n Integration Tutorial (with Webhooks) {#n8n-integration-tutorial-with-webhooks-en}

### Why Webhooks? {#why-webhooks-en}
Instead of having n8n ask our app "any new comments?" every few minutes (polling), our app instantly tells n8n when a new comment arrives. This is faster, more efficient, and real-time.

### Workflow Scenario {#workflow-scenario-en}
We want to build a workflow that:
1.  Triggers instantly when a comment with your keyword is received.
2.  Uses an AI service (like OpenAI) to generate a smart reply to the comment.
3.  Posts the generated response as a reply to the original comment on Instagram.

### Implementation Steps in n8n {#implementation-steps-in-n8n-en}

**Step 1: Create a Webhook Trigger in n8n**
-   Create a new n8n workflow.
-   Select `Webhook` as the first node.
-   A new Test URL will be generated by n8n. Copy it.

**Step 2: Register the Webhook in the App**
-   Go to your Instagram automation dashboard.
-   Paste the copied URL into the "Webhook Management" section and add it.

**Step 3: Send Sample Data to n8n**
-   On Instagram, post a comment with your keyword under the post you're automating.
-   Our app will instantly send the comment data to n8n, and the Webhook node will capture it.

**Step 4: Add an AI Node**
-   Add an `OpenAI` node (or any other service) to the workflow.
-   **Prompt**: `Generate a friendly and helpful reply to this Instagram comment: "{{ $json.body.text }}"`

**Step 5: Add an HTTP Request Node to Send the Reply**
-   Add an `HTTP Request` node to the workflow.
-   **Method**: `POST`
-   **URL**: `http://<YOUR_SERVER_IP>:<PORT>/api/automations/reply` **(This is a new endpoint to be added)**
-   **Authentication**: `Header Auth`.
    -   **Name**: `Authorization`
    -   **Value**: `Bearer {{ $credentials.apiToken.token }}` (Your token is the `sessionid` from login).
-   **Body (JSON)**:
    ```json
    {
      "comment_id": "{{ $json.body.pk }}",
      "reply_text": "{{ $json.choices[0].message.content }}"
    }
    ```
Your n8n workflow is now ready!

## 6. API Documentation {#api-documentation-en}
-   **Login**: `POST /api/login/credentials`, `POST /api/login/session`
-   **Task Management**: `GET /api/automations`, `POST /api/automations`, `DELETE /api/automations/{task_id}`
-   **Webhook Management**: `GET /api/webhooks`, `POST /api/webhooks`, `DELETE /api/webhooks`
-   **Send Reply**: `POST /api/automations/reply`
