
# Instagram Automation Tool - Comprehensive Guide

This document provides a complete, beginner-friendly guide to every aspect of the Instagram Automation Tool, from installation and basic use to advanced integration with n8n.

---

<details>
<summary>🇮🇷 **فهرست مطالب (برای باز شدن کلیک کنید)**</summary>

1.  [معرفی پروژه](#معرفی-پروژه-fa)
2.  [قابلیت‌های کلیدی](#قابلیت-های-کلیدی-fa)
3.  [معماری سیستم](#معماری-سیستم-fa)
4.  [راهنمای نصب](#راهنمای-نصب-fa)
    *   [پیش‌نیازها](#پیش-نیازها-fa)
    *   [نصب با Docker (روش پیشنهادی)](#نصب-با-docker-fa)
    *   [نصب با محیط مجازی پایتون (دستی)](#نصب-با-venv-fa)
5.  [راهنمای استفاده از رابط کاربری](#راهنمای-استفاده-از-رابط-کاربری-fa)
    *   [ورود به سیستم](#ورود-به-سیستم-fa)
    *   [مدیریت تسک‌های اتوماسیون](#مدیریت-تسک-ها-fa)
    *   [مدیریت Webhooks برای n8n](#مدیریت-webhook-ها-fa)
6.  [مستندات کامل API](#مستندات-کامل-api-fa)
    *   [احراز هویت](#احراز-هویت-fa)
    *   [مدیریت اتوماسیون](#مدیریت-اتوماسیون-fa)
    *   [مدیریت Webhook](#مدیریت-webhook-fa)
    *   [اندپوینت‌های بهینه شده برای n8n](#اندپوینت-های-بهینه-شده-برای-n8n-fa)
7.  [آموزش پیشرفته: یکپارچه‌سازی با n8n](#آموزش-پیشرفته-n8n-fa)
    *   [سناریوی نهایی](#سناریوی-نهایی-fa)
    *   [مراحل پیاده‌سازی و دیاگرام نودها](#مراحل-پیاده-سازی-و-دیاگرام-نودها-fa)

</details>

<details>
<summary>🇬🇧 **Table of Contents (Click to expand)**</summary>

1.  [Introduction](#introduction-en)
2.  [Core Features](#core-features-en)
3.  [System Architecture](#system-architecture-en)
4.  [Installation Guide](#installation-guide-en)
    *   [Prerequisites](#prerequisites-en)
    *   [Installation with Docker (Recommended)](#installation-with-docker-en)
    *   [Installation with Python venv (Manual)](#installation-with-venv-en)
5.  [Web UI User Guide](#web-ui-user-guide-en)
    *   [Logging In](#logging-in-en)
    *   [Managing Automation Tasks](#managing-tasks-en)
    *   [Managing n8n Webhooks](#managing-webhooks-en)
6.  [Complete API Documentation](#complete-api-documentation-en)
    *   [Authentication](#authentication-en)
    *   [Automation Management](#automation-management-en)
    *   [Webhook Management](#webhook-management-en)
    *   [n8n-Optimized Endpoints](#n8n-optimized-endpoints-en)
7.  [Advanced Tutorial: n8n Integration](#advanced-n8n-tutorial-en)
    *   [The Final Scenario](#the-final-scenario-en)
    *   [Implementation Steps & Node Diagrams](#implementation-steps--node-diagrams-en)

</details>

---

## 🇮🇷 مستندات فارسی (Farsi Documentation) {#معرفی-پروژه-fa}

### ۱. معرفی پروژه
این پروژه یک ابزار اتوماسیون اینستاگرام کامل و رایگان است که به شما اجازه می‌دهد وظایف تکراری مانند پاسخ به کامنت‌ها و ارسال دایرکت را به صورت خودکار انجام دهید. این ابزار با الهام از ManyChat، اما بدون نیاز به API رسمی اینستاگرام، ساخته شده و دارای رابط کاربری وب، نصب آسان با Docker، و قابلیت‌های قدرتمند برای یکپارچه‌سازی با پلتفرم‌هایی مانند n8n است. این سیستم کاملاً رایگان و متن باز است.

### ۲. قابلیت‌های کلیدی {#قابلیت-های-کلیدی-fa}
-   **ورود دوگانه**: امکان ورود امن به حساب کاربری با **نام کاربری و رمز عبور** یا **Session ID**.
-   **اتوماسیون هوشمند کامنت و دایرکت**: وظایfی تعریف کنید که بر اساس کلمات کلیدی در کامنت‌ها فعال شوند.
-   **پاسخ‌های چندگانه و تصادفی**: برای هر وظیفه، لیستی از پاسخ‌های مختلف برای کامنت و دایرکت تعریف کنید. سیستم به صورت خودکار یکی از آن‌ها را انتخاب می‌کند تا رفتار شما طبیعی‌تر به نظر برسد.
-   **شرط فالو داشتن**: اتوماسیون را فقط برای کاربرانی فعال کنید که صفحه شما را فالو می‌کنند.
-   **یکپارچه‌سازی لحظه‌ای با n8n (Webhook)**: به محض دریافت یک کامنت واجد شرایط، برنامه یک نوتیفیکیشن آنی به n8n ارسال می‌کند و گردش کار شما را فعال می‌کند.
-   **API دوگانه**: هر قابلیت برنامه هم از طریق یک اندپوینت استاندارد REST و هم از طریق یک اندپوینت جامع و بهینه‌شده برای n8n در دسترس است.
-   **نصب آسان**: اسکریپت نصب هوشمند (`install.sh`) که تمام مراحل را برای Docker و venv به صورت خودکار انجام می‌دهد و پورت‌ها را به صورت تعاملی از شما می‌پرسد.

### ۳. معماری سیستم {#معماری-سیستم-fa}
این برنامه از یک معماری میکروسرویس مبتنی بر Docker استفاده می‌کند که شامل سه بخش اصلی است:
1.  **Backend (FastAPI)**: هسته اصلی برنامه که با پایتون نوشته شده و مسئول ارتباط با اینستاگرام (از طریق کتابخانه `instagrapi`)، مدیریت منطق اتوماسیون و ارائه API است.
2.  **Frontend (Vanilla JS)**: یک رابط کاربری ساده و کارآمد که در مرورگر شما اجرا می‌شود و به شما اجازه می‌دهد تا وظایف و تنظیمات را به صورت گرافیکی مدیریت کنید.
3.  **Nginx**: به عنوان یک Reverse Proxy عمل می‌کند و درخواست‌های ورودی را به سرویس مناسب (Frontend یا Backend) هدایت می‌کند. این کار باعث افزایش امنیت و سادگی در مدیریت پورت‌ها می‌شود.

```
                  +-----------------------------------+
                  |      کاربر (User via Browser)      |
                  +-----------------------------------+
                                   |
                                   | HTTP/HTTPS Request on Port 80/443 (Configurable)
                                   v
+--------------------------------------------------------------------------+
|                        Docker Host (Your Server)                         |
|                                                                          |
|   +--------------------------+                                           |
|   |      Nginx Container     |                                           |
|   | (Listens on Port 8080)   |                                           |
|   |--------------------------|                                           |
|   |                          |-----> (Serves static files) ----> +--------------------+      |
|   |   / (Root URL)           |                                  | Frontend Container |      |
|   |                          |<----- (HTML, CSS, JS) <---------- | (No exposed port)  |      |
|   |                          |                                  +--------------------+      |
|   |--------------------------|                                                              |
|   |                          |-----> (Forwards API calls) ----> +--------------------+      |
|   |   /api/*                 |                                  |  Backend Container |      |
|   |                          |<----- (JSON Response) <--------- |  (FastAPI on 8000) |      |
|   |                          |                                  +--------------------+      |
|   +--------------------------+                                           |
|                                                                          |
+--------------------------------------------------------------------------+
```

### ۴. راهنمای نصب {#راهنمای-نصب-fa}

#### پیش‌نیازها {#پیش-نیازها-fa}
-   یک سرور یا کامپیوتر با سیستم‌عامل لینوکس (مانند Ubuntu 20.04+).
-   `Docker` و `Docker Compose` نصب شده باشند.
-   `Git` برای دانلود پروژه.
-   `Python 3.8+` و `pip` (فقط برای نصب دستی).

#### نصب با Docker (روش پیشنهادی) {#نصب-با-docker-fa}
این روش ساده‌ترین و پایدارترین راه برای اجرای برنامه است.
1.  **دانلود پروژه:**
    ```bash
    git clone https://github.com/your-repo/instagram-automation.git
    cd instagram-automation
    ```
2.  **اجرای اسکریپت نصب:**
    این اسکریپت به شما اجازه می‌دهد پورت‌ها و مسیر نصب را به صورت تعاملی تنظیم کنید.
    ```bash
    chmod +x install.sh
    sudo ./install.sh
    ```
    اسکریپت از شما سوالات زیر را خواهد پرسید:
    -   **روش نصب:** `docker` یا `venv` را انتخاب کنید. `docker` را وارد کنید.
    -   **مسیر نصب:** یک مسیر مطلق برای نصب برنامه انتخاب کنید (پیش‌فرض: `/opt/instagram_automation`).
    -   **پیکربندی پورت‌ها:** می‌توانید از پورت‌های پیش‌فرض استفاده کنید (`default`) یا آن‌ها را به صورت دستی (`manual`) وارد کنید. در حالت دستی، پورت وب (مثلاً `8080`) و پورت API (که توسط Nginx استفاده می‌شود) را مشخص خواهید کرد.
3.  **اتمام نصب:**
    اسکریپت به طور خودکار ایمیج‌های Docker را ساخته و کانتینرها را اجرا می‌کند. پس از اتمام، می‌توانید با مراجعه به آدرس `http://<YOUR_SERVER_IP>:<WEB_PORT>` به رابط کاربری دسترسی پیدا کنید.

#### نصب با محیط مجازی پایتون (دستی) {#نصب-با-venv-fa}
این روش برای توسعه‌دهندگان و کاربرانی که نمی‌خواهند از Docker استفاده کنند مناسب است.
1.  **دانلود و ورود به پوشه پروژه:**
    ```bash
    git clone https://github.com/your-repo/instagram-automation.git
    cd instagram-automation
    ```
2.  **اجرای اسکریپت نصب:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    -   در پاسخ به سوال اول، `venv` را انتخاب کنید.
    -   مسیر نصب و پورت‌های مورد نیاز برای Backend و Frontend را مشخص کنید.
3.  **اجرای برنامه:**
    اسکریپت دو سرویس `systemd` ایجاد می‌کند (`backend.service` و `frontend.service`) تا برنامه به صورت دائمی در پس‌زمینه اجرا شود. برای مدیریت سرویس‌ها می‌توانید از دستورات زیر استفاده کنید:
    ```bash
    sudo systemctl start backend
    sudo systemctl status backend
    sudo systemctl stop frontend
    ```

### ۵. راهنمای استفاده از رابط کاربری {#راهنمای-استفاده-از-رابط-کاربری-fa}

#### ورود به سیستم {#ورود-به-سیستم-fa}
-   **با نام کاربری و رمز عبور:** امن‌ترین روش است. اطلاعات شما ذخیره نمی‌شود و فقط برای ایجاد یک Session استفاده می‌شود.
-   **با Session JSON:** این روش پایدارترین راه برای استفاده از یک session موجود است، به خصوص اگر ورود دو مرحله‌ای دارید.
    -   **چگونه Session JSON را استخراج کنیم؟**
        1.  در یک مرورگر مبتنی بر کروم (مانند Chrome, Edge, Brave) وارد سایت `instagram.com` شوید.
        2.  افزونه مدیریت کوکی مانند **Cookie-Editor** را نصب کنید.
        3.  روی آیکون افزونه در نوار ابزار خود کلیک کنید.
        4.  گزینه **Export** را انتخاب کنید، سپس **Export as JSON** را بزنید. این کار یک فایل متنی را در کامپیوتر شما دانلود می‌کند.
        5.  محتوای کامل آن فایل را باز کرده، کپی کنید و در کادر "Session JSON" در برنامه ما پیست کنید.

#### مدیریت تسک‌های اتوماسیون {#مدیریت-تسک-ها-fa}
1.  **URL پست:** لینک پستی که می‌خواهید کامنت‌های آن را مانیتور کنید.
2.  **کلمات کلیدی:** لیستی از کلمات که با کاما (`,`) از هم جدا شده‌اند. اگر کامنتی حاوی یکی از این کلمات باشد، اتوماسیون فعال می‌شود.
3.  **پاسخ‌های کامنت/دایرکت:** در هر باکس، هر خط یک پاسخ مجزا است. سیستم به صورت تصادفی یکی از خطوط را انتخاب می‌کند.
4.  **شرط فالو:** اگر تیک زده شود، فقط به کامنت‌های فالوورهایتان پاسخ داده می‌شود.

#### مدیریت Webhooks برای n8n {#مدیریت-webhook-ها-fa}
در این بخش، URL وبهوک n8n خود را وارد کنید. هر زمان که یک کامنت جدید با شرایط تعریف شده مطابقت داشته باشد، یک درخواست `POST` با اطلاعات کامل کامنت (مانند متن، نام کاربری، ID کامنت و ID پست) به این URL ارسال می‌شود.

### ۶. مستندات کامل API {#مستندات-کامل-api-fa}
**Base URL:** `/api`

---

#### احراز هویت {#احراز-هویت-fa}

##### `POST /login/credentials`
ورود با نام کاربری و رمز عبور.
-   **Body:**
    ```json
    {
      "username": "YOUR_USERNAME",
      "password": "YOUR_PASSWORD"
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "message": "Successfully logged in."
    }
    ```
-   **Error Response (401):**
    ```json
    {
      "message": "Login failed: Challenge required"
    }
    ```

##### `POST /login/session`
ورود با Session ID.
-   **Body:**
    ```json
    {
      "session_id": "YOUR_SESSION_ID_STRING"
    }
    ```

---

#### مدیریت اتوماسیون {#مدیریت-اتوماسیون-fa}

##### `POST /automations`
ایجاد یک تسک اتوماسیون جدید.
-   **Body:**
    ```json
    {
      "post_url": "https://www.instagram.com/p/Cxyz...",
      "keywords": ["awesome", "great"],
      "comment_replies": ["Thanks!", "Glad you liked it!"],
      "dm_replies": ["Thanks for your comment!", "We saw your message."],
      "followers_only": true
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "task_id": "unique_task_id_123",
      "message": "Automation task started successfully."
    }
    ```

##### `GET /automations`
دریافت لیست تمام تسک‌های فعال.

##### `DELETE /automations/{task_id}`
حذف یک تسک.

---

#### مدیریت Webhook {#مدیریت-webhook-fa}

##### `POST /webhooks`
افزودن یک URL وبهوک جدید.
-   **Body:**
    ```json
    {
      "url": "https://your.n8n.instance/webhook/123"
    }
    ```

##### `GET /webhooks`
دریافت لیست وبهوک‌های ثبت‌شده.

##### `DELETE /webhooks`
حذف یک وبهوک.
-   **Body:**
    ```json
    {
      "url": "https://your.n8n.instance/webhook/123"
    }
    ```
---

#### نمونه‌های کد {#کد-نمونه-fa}

**JavaScript (Fetch API):**
```javascript
async function loginAndAddTask() {
  const API_URL = 'http://localhost:8080/api';

  // Login
  const loginResponse = await fetch(`${API_URL}/login/credentials`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'testuser', password: 'testpassword' })
  });
  console.log('Login Status:', loginResponse.status);

  // Add Task
  const taskData = {
    post_url: "https://www.instagram.com/p/Cxyz...",
    keywords: ["test", "automation"],
    comment_replies": ["This is a test reply."],
    dm_replies": ["This is a test DM."],
    followers_only": false
  };

  const taskResponse = await fetch(`${API_URL}/automations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  const result = await taskResponse.json();
  console.log('Add Task Result:', result);
}
```

**.NET (HttpClient):**
```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class InstagramApiClient
{
    private readonly HttpClient _httpClient;
    private const string ApiBaseUrl = "http://localhost:8080/api";

    public InstagramApiClient()
    {
        _httpClient = new HttpClient();
    }

    public async Task LoginAsync(string username, string password)
    {
        var loginData = new { username, password };
        var json = JsonConvert.SerializeObject(loginData);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync($"{ApiBaseUrl}/login/credentials", content);
        response.EnsureSuccessStatusCode();
        Console.WriteLine("Login successful!");
    }
}
```

### ۷. آموزش پیشرفته: یکپارچه‌سازی با n8n {#آموزش-پیشرفته-n8n-fa}

#### سناریوی نهایی {#سناریوی-نهایی-fa}
ما یک گردش کار (Workflow) بسیار پیشرفته در n8n طراحی می‌کنیم که فرآیند پاسخ به کامنت‌ها را با استفاده از هوش مصنوعی و ردیابی کاربر در Google Sheets به طور کامل خودکار می‌کند. این گردش کار به طور خاص برای مدیریت تعاملات در پست‌های مسابقه یا کمپین‌ها طراحی شده است.

**منطق گردش کار:**
1.  **دریافت کامنت:** گردش کار با دریافت یک نوتیفیکیشن از برنامه ما از طریق وبهوک آغاز می‌شود.
2.  **بررسی کاربر در Google Sheets:** بررسی می‌کند آیا نام کاربری که کامنت گذاشته، قبلاً در فایل Google Sheets ما ثبت شده است یا خیر.
3.  **بررسی وضعیت فالو (Follow):** از API داخلی برنامه ما استفاده می‌کند تا بفهمد آیا کاربر، پیج ما را فالو می‌کند یا خیر.
4.  **منطق شرطی پیچیده (IF):**
    *   **اگر کاربر فالوور نباشد:** یک پیام دایرکت (DM) محترمانه برای او ارسال می‌کند و از او می‌خواهد که برای شرکت در مسابقه، پیج را فالو کند.
    *   **اگر کاربر فالوور باشد اما قبلاً کامنت گذاشته باشد:** یک پاسخ استاندارد (که به صورت تصادفی از لیستی انتخاب شده) برای کامنت او ارسال می‌کند تا از ارسال پیام‌های تکراری جلوگیری شود.
    *   **اگر کاربر فالوور باشد و اولین کامنت او باشد:**
        1.  نام کاربری او را در Google Sheets ثبت می‌کند.
        2.  با استفاده از OpenAI یک پاسخ خلاقانه و جذاب برای کامنت او تولید می‌کند.
        3.  پاسخ تولید شده توسط AI را به عنوان ریپلای برای کامنت او ارسال می‌کند.

#### مراحل پیاده‌سازی و دیاگرام نودها {#مراحل-پیاده-سازی-و-دیاگرام-نودها-fa}

**Node 1: Webhook**
-   یک نود `Webhook` ایجاد کنید و URL آن را در رابط کاربری برنامه ما ثبت کنید.
-   یک کامنت تستی بفرستید تا داده‌های نمونه (`comment_id`, `comment_text`, `username`, `user_id`) دریافت شوند.

**Node 2: Google Sheets (Search)**
-   یک نود `Google Sheets` با عملیات `Lookup` (یا `Get Many`) اضافه کنید تا `username` را در شیت شرکت‌کنندگان جستجو کند.

**Node 3: HTTP Request (Check Follower Status)**
-   یک نود `HTTP Request` برای فراخوانی API داخلی برنامه ما اضافه کنید.
-   **URL:** `http://<YOUR_SERVER_IP>:<WEB_PORT>/api/n8n/user/is-follower`
-   **Method:** `POST`
-   **Body (JSON):** `{ "user_id": "{{ $json.body.user_id }}" }`
-   این اندپوینت یک پاسخ `true` یا `false` برمی‌گرداند. *نکته: شما باید این اندپوینت را به `main.py` و `instagram_client.py` اضافه کنید.*

**Node 4: IF Node (Main Logic)**
-   این نود سه مسیر خروجی خواهد داشت:
    1.  **No Follow:** `{{ $('HTTP Request').item.json.is_follower }}` -> `is` -> `false`
    2.  **Already Entered:** `{{ $items('Google Sheets').length }}` -> `is not` -> `0`
    3.  **New Entry (Default):** مسیر `true` برای بقیه موارد.

**مسیر 1 (کاربر فالوور نیست):**

**Node 5a: HTTP Request (Send "Please Follow" DM)**
-   **URL:** `http://<YOUR_SERVER_IP>:<WEB_PORT>/api/n8n/dm/send`
-   **Method:** `POST`
-   **Body (JSON):**
    ```json
    {
      "user_id": "{{ $json.body.user_id }}",
      "text": "سلام! ممنون از کامنت شما. برای شرکت در مسابقه، لطفاً پیج ما را فالو کنید."
    }
    ```
    *نکته: شما باید این اندپوینت را نیز به backend اضافه کنید.*

**مسیر 2 (کاربر قبلاً شرکت کرده):**

**Node 5b: Set Random Reply**
-   یک نود `Set` برای انتخاب یک پاسخ تصادفی از یک لیست. (مشابه مثال قبلی)

**Node 6b: HTTP Request (Send Standard Reply)**
-   یک نود `HTTP Request` برای ارسال پاسخ استاندارد از طریق اندپوینت `/api/n8n/automations/reply`.

**مسیر 3 (کاربر جدید و فالوور):**

**Node 5c: Google Sheets (Append)**
-   یک نود `Google Sheets` برای اضافه کردن `username` به شیت.

**Node 6c: OpenAI (Generate AI Reply)**
-   یک نود `OpenAI` برای تولید یک پاسخ خلاقانه بر اساس متن کامنت کاربر (`comment_text`).

**Node 7c: HTTP Request (Send AI Reply)**
-   یک نود `HTTP Request` برای ارسال پاسخ تولید شده توسط AI از طریق اندپوینت `/api/n8n/automations/reply`.

این گردش کار بسیار قدرتمندتر است و تمام جنبه‌های تعامل با کاربر را به صورت هوشمند مدیریت می‌کند و دقیقاً همان چیزی است که برای یک کمپین حرفه‌ای نیاز دارید.

---
---

## 🇬🇧 English Documentation {#introduction-en}

### 1. Introduction
This project is a complete, free Instagram automation tool that allows you to automate repetitive tasks like replying to comments and sending DMs. Inspired by ManyChat but without needing the official Instagram API, it features a web UI, easy Docker installation, and powerful integration capabilities with platforms like n8n. This system is entirely free and open-source.

### 2. Core Features {#core-features-en}
-   **Dual Login**: Securely log in with **username and password** or a **Session ID**.
-   **Smart Comment & DM Automation**: Define tasks that trigger based on keywords in comments.
-   **Multiple & Randomized Replies**: For each task, define a list of different replies for comments and DMs. The system will randomly pick one to make your interactions feel more natural.
-   **Follower Condition**: Optionally restrict automation to only run for users who follow your page.
-   **Real-time n8n Integration (Webhooks)**: As soon as a matching comment is received, the app sends an instant notification to trigger your n8n workflow.
-   **Dual API**: Every feature is accessible via both a standard REST endpoint and a unified, n8n-optimized endpoint.
-   **Easy Installation**: A smart `install.sh` script that automates the entire setup for both Docker and venv, including interactive prompts for port configuration.

### 3. System Architecture {#system-architecture-en}
The application uses a Docker-based microservice architecture consisting of three main components:
1.  **Backend (FastAPI)**: The core of the application, written in Python. It handles communication with Instagram (via the `instagrapi` library), manages automation logic, and exposes the API.
2.  **Frontend (Vanilla JS)**: A clean and efficient user interface that runs in your browser, allowing you to graphically manage tasks and settings.
3.  **Nginx**: Acts as a reverse proxy, directing incoming requests to the appropriate service (Frontend or Backend). This enhances security and simplifies port management.

(See the architecture diagram in the Farsi section above)

### 4. Installation Guide {#installation-guide-en}

#### Prerequisites {#prerequisites-en}
-   A Linux-based server or machine (e.g., Ubuntu 20.04+).
-   `Docker` and `Docker Compose` installed.
-   `Git` for cloning the project.
-   `Python 3.8+` and `pip` (for manual installation only).

#### Installation with Docker (Recommended) {#installation-with-docker-en}
This is the simplest and most stable way to run the application.
1.  **Clone the project:**
    ```bash
    git clone https://github.com/your-repo/instagram-automation.git
    cd instagram-automation
    ```
2.  **Run the installation script:**
    This script allows you to interactively configure ports and the installation path.
    ```bash
    chmod +x install.sh
    sudo ./install.sh
    ```
    The script will ask you the following:
    -   **Installation Method:** Choose `docker` or `venv`. Enter `docker`.
    -   **Installation Path:** Choose an absolute path for the installation (default: `/opt/instagram_automation`).
    -   **Port Configuration:** You can use the `default` ports or set them `manual`ly. In manual mode, you'll specify the web port (e.g., `8080`) and the API port used by Nginx.
3.  **Finish Installation:**
    The script will automatically build the Docker images and start the containers. Once finished, you can access the UI by navigating to `http://<YOUR_SERVER_IP>:<WEB_PORT>`.

#### Installation with Python venv (Manual) {#installation-with-venv-en}
This method is suitable for developers or users who prefer not to use Docker.
1.  **Clone and enter the project directory:**
    ```bash
    git clone https://github.com/your-repo/instagram-automation.git
    cd instagram-automation
    ```
2.  **Run the installation script:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    -   When prompted, choose `venv`.
    -   Specify the installation path and the required ports for the Backend and Frontend.
3.  **Running the Application:**
    The script creates two `systemd` services (`backend.service` and `frontend.service`) to run the application persistently in the background. You can manage them with commands like:
    ```bash
    sudo systemctl start backend
    sudo systemctl status backend
    sudo systemctl stop frontend
    ```

### 5. Web UI User Guide {#web-ui-user-guide-en}

#### Logging In {#logging-in-en}
-   **With Username & Password:** This is the most secure method. Your credentials are not stored and are only used to create a session.
-   **With Session JSON:** This is the most stable method for using an existing session, especially if you have two-factor authentication enabled.
    -   **How to export your Session JSON?**
        1.  In a Chromium-based browser (like Chrome, Edge, Brave), log into `instagram.com`.
        2.  Install a cookie manager extension, such as **Cookie-Editor**.
        3.  Click the extension's icon in your toolbar.
        4.  Choose **Export**, then **Export as JSON**. This will download a text file to your computer.
        5.  Open that file, copy its entire contents, and paste it into the "Session JSON" field in our application.

#### Managing Automation Tasks {#managing-tasks-en}
1.  **Post URL:** The link to the post whose comments you want to monitor.
2.  **Keywords:** A comma-separated list of words. The automation will trigger if a comment contains any of these words.
3.  **Comment/DM Replies:** In each textbox, every new line is a separate reply. The system will randomly pick one.
4.  **Follower Condition:** If checked, the bot will only reply to comments from your followers.

#### Managing n8n Webhooks {#managing-webhooks-en}
Enter your n8n webhook URL here. Whenever a new comment matches the defined criteria, a `POST` request containing the full comment data (text, username, comment ID, post ID) will be sent to this URL.

### 6. Complete API Documentation {#complete-api-documentation-en}
**Base URL:** `/api`

---

#### Authentication {#authentication-en}

##### `POST /login/credentials`
Login with a username and password.
-   **Body:**
    ```json
    {
      "username": "YOUR_USERNAME",
      "password": "YOUR_PASSWORD"
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "message": "Successfully logged in."
    }
    ```
-   **Error Response (401):**
    ```json
    {
      "message": "Login failed: Challenge required"
    }
    ```

##### `POST /login/session`
Login with a Session ID.
-   **Body:**
    ```json
    {
      "session_id": "YOUR_SESSION_ID_STRING"
    }
    ```

---

#### Automation Management {#automation-management-en}

##### `POST /automations`
Create a new automation task.
-   **Body:**
    ```json
    {
      "post_url": "https://www.instagram.com/p/Cxyz...",
      "keywords": ["awesome", "great"],
      "comment_replies": ["Thanks!", "Glad you liked it!"],
      "dm_replies": ["Thanks for your comment!", "We saw your message."],
      "followers_only": true
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "task_id": "unique_task_id_123",
      "message": "Automation task started successfully."
    }
    ```

##### `GET /automations`
Get a list of all active tasks.

##### `DELETE /automations/{task_id}`
Delete a task.

---

#### Webhook Management {#webhook-management-en}

##### `POST /webhooks`
Add a new webhook URL.
-   **Body:**
    ```json
    {
      "url": "https://your.n8n.instance/webhook/123"
    }
    ```

##### `GET /webhooks`
Get the list of registered webhooks.

##### `DELETE /webhooks`
Delete a webhook.
-   **Body:**
    ```json
    {
      "url": "https://your.n8n.instance/webhook/123"
    }
    ```
---

#### Code Examples {#code-examples-en}

**JavaScript (Fetch API):**
```javascript
async function loginAndAddTask() {
  const API_URL = 'http://localhost:8080/api';

  // Login
  const loginResponse = await fetch(`${API_URL}/login/credentials`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'testuser', password: 'testpassword' })
  });
  console.log('Login Status:', loginResponse.status);

  // Add Task
  const taskData = {
    post_url: "https://www.instagram.com/p/Cxyz...",
    keywords: ["test", "automation"],
    comment_replies: ["This is a test reply."],
    dm_replies: ["This is a test DM."],
    followers_only: false
  };

  const taskResponse = await fetch(`${API_URL}/automations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  const result = await taskResponse.json();
  console.log('Add Task Result:', result);
}
```

**.NET (HttpClient):**
```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class InstagramApiClient
{
    private readonly HttpClient _httpClient;
    private const string ApiBaseUrl = "http://localhost:8080/api";

    public InstagramApiClient()
    {
        _httpClient = new HttpClient();
    }

    public async Task LoginAsync(string username, string password)
    {
        var loginData = new { username, password };
        var json = JsonConvert.SerializeObject(loginData);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync($"{ApiBaseUrl}/login/credentials", content);
        response.EnsureSuccessStatusCode();
        Console.WriteLine("Login successful!");
    }
}
```

### 7. Advanced Tutorial: n8n Integration {#advanced-n8n-tutorial-en}

#### The Final Scenario {#the-final-scenario-en}
We will design a highly advanced n8n workflow that fully automates the process of replying to comments using AI and tracking users in Google Sheets. This workflow is specifically designed for managing interactions on contest or campaign posts.

**Workflow Logic:**
1.  **Receive Comment:** The workflow starts when it receives a notification from our app via a webhook.
2.  **Check User in Google Sheets:** It checks if the username that commented is already in our Google Sheet of participants.
3.  **Check Follower Status:** It uses our app's internal API to determine if the user is following our page.
4.  **Complex Conditional Logic (IF):**
    *   **If the user is NOT a follower:** It sends a polite Direct Message (DM) asking them to follow the page to enter the contest.
    *   **If the user IS a follower but has already commented:** It sends a standard reply (randomly selected from a list) to their comment to avoid spamming them.
    *   **If the user IS a follower and this is their first comment:**
        1.  It registers their username in the Google Sheet.
        2.  It uses OpenAI to generate a creative and engaging reply to their comment.
        3.  It posts the AI-generated response as a reply to their comment.

#### Implementation Steps & Node Diagrams {#implementation-steps--node-diagrams-en}

**Node 1: Webhook**
-   Create a `Webhook` node and register its URL in our app's UI.
-   Send a test comment to receive sample data (`comment_id`, `comment_text`, `username`, `user_id`).

**Node 2: Google Sheets (Search)**
-   Add a `Google Sheets` node with the `Lookup` (or `Get Many`) operation to search for the `username` in your participants sheet.

**Node 3: HTTP Request (Check Follower Status)**
-   Add an `HTTP Request` node to call our app's internal API.
-   **URL:** `http://<YOUR_SERVER_IP>:<WEB_PORT>/api/n8n/user/is-follower`
-   **Method:** `POST`
-   **Body (JSON):** `{ "user_id": "{{ $json.body.user_id }}" }`
-   This endpoint will return `true` or `false`. *Note: You will need to add this endpoint to `main.py` and `instagram_client.py`.*

**Node 4: IF Node (Main Logic)**
-   This node will have three output paths:
    1.  **No Follow:** `{{ $('HTTP Request').item.json.is_follower }}` -> `is` -> `false`
    2.  **Already Entered:** `{{ $items('Google Sheets').length }}` -> `is not` -> `0`
    3.  **New Entry (Default):** The `true` path for all other cases.

**Path 1 (User is Not a Follower):**

**Node 5a: HTTP Request (Send "Please Follow" DM)**
-   **URL:** `http://<YOUR_SERVER_IP>:<WEB_PORT>/api/n8n/dm/send`
-   **Method:** `POST`
-   **Body (JSON):**
    ```json
    {
      "user_id": "{{ $json.body.user_id }}",
      "text": "Hi! Thanks for your comment. To participate in the contest, please make sure you're following our page."
    }
    ```
    *Note: You will also need to add this endpoint to the backend.*

**Path 2 (User has Already Entered):**

**Node 5b: Set Random Reply**
-   Add a `Set` node to choose a random reply from a list (see previous example).

**Node 6b: HTTP Request (Send Standard Reply)**
-   Add an `HTTP Request` node to send the standard reply via the `/api/n8n/automations/reply` endpoint.

**Path 3 (New User and is a Follower):**

**Node 5c: Google Sheets (Append)**
-   Add a `Google Sheets` node to append the `username` to the sheet.

**Node 6c: OpenAI (Generate AI Reply)**
-   Add an `OpenAI` node to generate a creative reply based on the user's `comment_text`.

**Node 7c: HTTP Request (Send AI Reply)**
-   Add an `HTTP Request` node to send the AI-generated reply via the `/api/n8n/automations/reply` endpoint.

This workflow is far more powerful and intelligently handles all aspects of user interaction, making it exactly what you need for a professional campaign.
