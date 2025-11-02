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
    1.  `send_dm`:
        -   **Payload**: `{ "user_id": "12345", "text": "Hello!" }`
    2.  `post_comment`:
        -   **Payload**: `{ "media_id": "12345", "text": "Great post!" }`
    3.  `get_media_comments`:
        -   **Payload**: `{ "media_id": "12345", "amount": 30 }`
    4.  `get_user_posts`:
        -   **Payload**: `{ "user_id": 12345, "amount": 10 }` (Note: `user_id` is the numeric PK, not the username)
    5.  `check_follower_status`:
        -   **Payload**: `{ "target_user_id": 12345 }`

## Connecting with n8n (Advanced Tutorial)

This tutorial guides you through creating a powerful, rule-based workflow that intelligently responds to comments on your latest posts using Google Sheets and an AI agent.

### Prerequisite: Logging In

Before you can run the main workflow, you **must** log in to your Instagram account via the API. This is a **one-time setup**. The application will keep you logged in for all future actions.

**Create a simple, separate workflow in n8n for this purpose.**

#### Method: Login with Session JSON (Recommended)

```
+-------------------------------------------------------------------+
| [1] Manual Start Node                                             |
| Description: Executes the workflow manually just once.            |
+-------------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------------+
| [2] HTTP Request Node: "Login to Instagram"                       |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Request Method:    POST               (Mode: Fixed)             |
|   URL:               http://localhost:8000/login/session (Mode: Fixed) |
|   Authentication:    None                                         |
|   Body Content Type: JSON               (Mode: Fixed)             |
|   JSON/RAW Parameters:                                            |
|     - Key: session_data               (Mode: Fixed)             |
|     - Value: (Paste your full JSON object here) (Mode: Fixed)     |
|       {                                                           |
|         "sessionid": "...",                                       |
|         "ds_user_id": "...",                                       |
|         "csrftoken": "...",                                        |
|         "rur": "...",                                              |
|         "mid": "..."                                               |
|       }                                                           |
+-------------------------------------------------------------------+
```
> **Action**: Create this workflow, paste your complete session JSON data, and click "Execute Workflow". If it runs successfully, you are logged in. You do not need to run this again unless the session expires.

### Advanced Workflow: Smart, Rule-Based Comment Replies

This workflow will:
1.  Run on a schedule.
2.  Fetch your latest Instagram posts.
3.  For each post, fetch its comments.
4.  Filter out comments that you have already replied to.
5.  Check a Google Sheet for a matching rule (based on post link, keywords, and follower status).
6.  If a rule matches, reply using the text from the Google Sheet.
7.  If not, generate a reply using an AI agent.

#### Overall Workflow Diagram

```
[Cron] -> [Get Posts] -> [Split Posts] -> [Get Comments] -> [Split Comments] -> [Filter Replied] -> [Read Sheet] -> [IF: Rule Found?]
                                                                                                                   |
                                                                                               +-------------------+-------------------+
                                                                                               | (TRUE)                            | (FALSE)
                                                                                               v                                   v
                                                                        [Code: Keyword Match?] -> [IF: Keyword Match?]         [AI Agent]
                                                                                               |         | (TRUE)                  |
                                                                                               |         v                         |
                                                                          (FALSE)|         [Check Follower] -> [IF: Follower?]   |
                                                                                               |         | (TRUE)      | (FALSE)   |
                                                                                               |         v             v           |
                                                                                               |   [Reply Custom]  [Reply "Follow"]|
                                                                                               |         |             |           |
                                                                                               +---------+-------------+-----------+
                                                                                                         |
                                                                                                         v
                                                                                                     [Post AI Reply]
```

#### Step-by-Step Node Configuration

*(This is a detailed guide. Each step corresponds to a node in n8n.)*

**1. Cron Node: "Schedule Trigger"**
*This starts the workflow automatically.*
```
+-------------------------------------------------------------------+
| [1] Cron Node                                                     |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Mode:           Every X Minutes     (Mode: Fixed)             |
|   Minutes:        15                  (Mode: Fixed)             |
+-------------------------------------------------------------------+
```

**2. HTTP Request Node: "Get Latest Posts"**
*Fetches the most recent posts from your own Instagram account.*
```
+-------------------------------------------------------------------+
| [2] HTTP Request Node: "Get Latest Posts"                         |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Request Method:    POST               (Mode: Fixed)             |
|   URL:               http://localhost:8000/api/n8n/action (Mode: Fixed) |
|   Body Content Type: JSON               (Mode: Fixed)             |
|   JSON/RAW Parameters:                                            |
|     - Key: action                   (Mode: Fixed)             |
|     - Value: get_user_posts         (Mode: Fixed)             |
|     - Key: payload                  (Mode: Fixed)             |
|     - Value: { "amount": 5 }        (Mode: Fixed)             |
| Options:                                                          |
|   Split Into:     Items               (Mode: Fixed)             |
|   Path:           data                (Mode: Fixed)             |
+-------------------------------------------------------------------+
```

**3. HTTP Request Node: "Get Comments for Post"**
*For each post from the previous step, this fetches its comments.*
```
+-------------------------------------------------------------------+
| [3] HTTP Request Node: "Get Comments for Post"                    |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Request Method:    POST               (Mode: Fixed)             |
|   URL:               http://localhost:8000/api/n8n/action (Mode: Fixed) |
|   Body Content Type: JSON               (Mode: Fixed)             |
|   JSON/RAW Parameters:                                            |
|     - Key: action                   (Mode: Fixed)             |
|     - Value: get_media_comments     (Mode: Fixed)             |
|     - Key: payload                  (Mode: Expression)        |
|     - Value: { "media_id": "{{ $json.pk }}" }                   |
| Options:                                                          |
|   Split Into:     Items               (Mode: Fixed)             |
|   Path:           data                (Mode: Fixed)             |
+-------------------------------------------------------------------+
```
> **Data Flow**: The `media_id` is dynamically taken from the output of the "Get Latest Posts" node. `{{ $json.pk }}` refers to the 'pk' field of each post.

**4. Code Node: "Filter Out Replied Comments"**
*This simple code node checks if you have already replied to a comment and stops the workflow for that comment if you have.*
```
+-------------------------------------------------------------------+
| [4] Code Node: "Filter Out Replied Comments"                      |
+-------------------------------------------------------------------+
| Language:       JavaScript                                        |
| Code:                                                             |
|   const hasReplied = $json.has_liked; // A proxy for replies      |
|   if (hasReplied) {                                               |
|     return null; // Stop execution for this item                  |
|   }                                                               |
|   return $json; // Continue if not replied                        |
+-------------------------------------------------------------------+
```

**5. Google Sheets Node: "Read Rules from Sheet"**
*This node looks up rules in a spreadsheet.*
> **Setup**: Create a Google Sheet with columns: `PostURL`, `Keywords`, `FollowerOnly`, `CommentReply`, `DMReply`.

```
+-------------------------------------------------------------------+
| [5] Google Sheets Node: "Read Rules from Sheet"                   |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Authentication:    Connect your Google Account                  |
|   Resource:          Row                                          |
|   Operation:         Lookup                                       |
|   Spreadsheet:       Select your spreadsheet                      |
|   Sheet:             Select your sheet                            |
|   Column To Match On: PostURL             (Mode: Fixed)             |
|   Value To Match:    {{ "https://www.instagram.com/p/" + $('Get Comments for Post').json.code + "/" }} (Mode: Expression) |
+-------------------------------------------------------------------+
```

**6. IF Node: "Rule Found?"**
*Checks if the Google Sheet node found a matching rule.*
```
+-------------------------------------------------------------------+
| [6] IF Node: "Rule Found?"                                        |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - Condition 1:                                                  |
|     - Value 1: {{ $('Read Rules from Sheet').json.Keywords }} (Mode: Expression)|
|     - Operation: Is Not Empty                                     |
+-------------------------------------------------------------------+
```

From this IF node, there are two branches: **TRUE** (a rule was found) and **FALSE** (no rule found).

#### TRUE Branch (Rule-Based Reply)

**7a. Code Node: "Check if Keywords Match"**
*If a rule was found, this node checks if the comment text contains any of the keywords from the sheet.*
```
+-------------------------------------------------------------------+
| [7a] Code Node: "Check if Keywords Match"                         |
+-------------------------------------------------------------------+
| Language:       JavaScript                                        |
| Code:                                                             |
|   const keywords = $('Read Rules from Sheet').json.Keywords.split(','); |
|   const commentText = $('Filter Out Replied Comments').json.text.toLowerCase(); |
|   const match = keywords.some(k => commentText.includes(k.trim())); |
|   return { ...$item.json, ruleMatched: match };                   |
+-------------------------------------------------------------------+
```

**8a. IF Node: "Keyword Match?"**
*Connect this to the output of the previous Code node. It proceeds only if `ruleMatched` is true.*
```
+-------------------------------------------------------------------+
| [8a] IF Node: "Keyword Match?"                                    |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - Condition 1:                                                  |
|     - Value 1: {{ $json.ruleMatched }} (Mode: Expression)         |
|     - Operation: Is True                                          |
+-------------------------------------------------------------------+
```

**9a. HTTP Request Node: "Check Follower Status"**
*Connect to the **TRUE** output of "Keyword Match?". This checks if the commenter follows you.*
```
+-------------------------------------------------------------------+
| [9a] HTTP Request: "Check Follower Status"                        |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Request Method:    POST               (Mode: Fixed)             |
|   URL:               http://localhost:8000/api/n8n/action (Mode: Fixed) |
|   Body Content Type: JSON               (Mode: Fixed)             |
|   Body:                                                           |
|     - action: check_follower_status     (Mode: Fixed)             |
|     - payload: { "target_user_id": "{{ $('Filter Out Replied Comments').json.user.pk }}" } (Mode: Expression) |
+-------------------------------------------------------------------+
```

**10a. IF Node: "Is Follower?"**
*This node decides the reply based on the follower status and the rule in the sheet.*
```
+-------------------------------------------------------------------+
| [10a] IF Node: "Is Follower?"                                     |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - Condition 1:                                                  |
|     - Value 1: {{ $('Read Rules from Sheet').json.FollowerOnly }} (Mode: Expression)|
|     - Operation: Is False                                         |
|   - Condition 2 (OR):                                             |
|     - Value 1: {{ $('Check Follower Status').json.is_follower }} (Mode: Expression)|
|     - Operation: Is True                                          |
+-------------------------------------------------------------------+
```

**11a. HTTP Request Node: "Post Custom Reply"**
*Connect to the **TRUE** output of "Is Follower?". This sends the main reply.*
```
+-------------------------------------------------------------------+
| [11a] HTTP Request: "Post Custom Reply"                           |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('Filter Out Replied Comments').json.media.pk }}", "text": "{{ $('Read Rules from Sheet').json.CommentReply }}" } (Mode: Expression)|
+-------------------------------------------------------------------+
```

**12a. HTTP Request Node: "Post 'Please Follow' Reply"**
*Connect to the **FALSE** output of "Is Follower?". This sends the alternative reply.*
```
+-------------------------------------------------------------------+
| [12a] HTTP Request: "Post 'Please Follow' Reply"                  |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('Filter Out Replied Comments').json.media.pk }}", "text": "Please follow us to get a reply!" } (Mode: Expression)|
+-------------------------------------------------------------------+
```

#### FALSE Branch (AI-Powered Reply)

**7b. OpenAI Node: "Generate AI Reply"**
*Connect this to the **FALSE** output of "Rule Found?".*
```
+-------------------------------------------------------------------+
| [7b] OpenAI Node: "Generate AI Reply"                             |
+-------------------------------------------------------------------+
| Parameters:                                                       |
|   Resource:       Chat                                            |
|   Model:          gpt-4o                                          |
|   Prompt:         Based on this comment: "{{ $('Filter Out Replied Comments').json.text }}", write a helpful reply. |
+-------------------------------------------------------------------+
```

**8b. HTTP Request Node: "Post AI Reply"**
*Connect this node to the output of the OpenAI node.*
```
+-------------------------------------------------------------------+
| [8b] HTTP Request Node: "Post AI Reply"                           |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('Filter Out Replied Comments').json.media.pk }}", "text": "{{ $('Generate AI Reply').json.choices[0].message.content }}" } (Mode: Expression)|
+-------------------------------------------------------------------+
```
---
- [Project Structure](#project-structure)
---

# Farsi Documentation (مستندات فارسی)

یک ابزار اتوماسیون اینستاگرام متن-باز و سلف-هاست (قابل میزبانی روی سرور شخصی) که مشابه ManyChat عمل می‌کند، با این تفاوت که نیازی به کلید API رسمی اینستاگرام ندارد. این پروژه یک API در Backend و یک رابط کاربری ساده در Frontend برای مدیریت تسک‌های اتوماسیون کامنت و دایرکت فراهم می‌کند.

این پروژه از کتابخانه `instagrapi` برای ارتباط با اینستاگرام استفاده کرده و به راحتی با استفاده از Docker قابل راه‌اندازی است.

---

## فهرست مطالب

- [قابلیت‌ها](#قابلیت‌ها)
- [شیوه عملکرد](#شیوه-عملکرد)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [راهنمای استفاده](#راهنمای-استفاده)
- [مستندات API](#مستندات-api)
- [آموزش پیشرفته اتصال به n8n](#آموزش-پیشرفته-اتصال-به-n8n)
  - [پیش‌نیاز: لاگین به اینستاگرام](#پیش‌نیاز-لاگین-به-اینستاگرام)
  - [ورک‌فلو پیشرفته: پاسخ هوشمند و قانون‌مند به کامنت‌ها](#ورک‌فلو-پیشرفته-پاسخ-هوشمند-و-قانون‌مند-به-کامنت‌ها)

---

## (بخش‌های معرفی، قابلیت‌ها، نصب و راهنمای استفاده همانند نسخه قبلی باقی می‌مانند) ...

---

## آموزش پیشرفته اتصال به n8n

این آموزش شما را قدم به قدم در ساخت یک ورک‌فلو قدرتمند و قانون‌مند راهنمایی می‌کند که به صورت هوشمند و با استفاده از Google Sheets و یک عامل هوش مصنوعی، به کامنت‌های آخرین پست‌های شما پاسخ می‌دهد.

### پیش‌نیاز: لاگین به اینستاگرام

قبل از اینکه بتوانید ورک‌فلو اصلی را اجرا کنید، **باید** از طریق API به حساب اینستاگرام خود لاگین کنید. این یک **تنظیمات یک‌باره** است. اپلیکیشن شما را برای تمام اقدامات بعدی لاگین نگه می‌دارد.

**برای این کار، یک ورک‌فلو ساده و مجزا در n8n بسازید.**

#### روش پیشنهادی: ورود با Session JSON

```
+-------------------------------------------------------------------+
| [1] نود Manual Start (شروع دستی)                                  |
| توضیحات: این ورک‌فلو را به صورت دستی فقط یک بار اجرا می‌کند.         |
+-------------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------------+
| [2] نود HTTP Request: "ورود به اینستاگرام"                         |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Request Method:    POST               (حالت: Fixed)            |
|   URL:               http://localhost:8000/login/session (حالت: Fixed) |
|   Authentication:    None                                         |
|   Body Content Type: JSON               (حالت: Fixed)            |
|   JSON/RAW Parameters:                                            |
|     - کلید (Key): session_data          (حالت: Fixed)            |
|     - مقدار (Value): (آبجکت کامل JSON خود را اینجا وارد کنید) (حالت: Fixed) |
|       {                                                           |
|         "sessionid": "...",                                       |
|         "ds_user_id": "...",                                       |
|         "csrftoken": "...",                                        |
|         "rur": "...",                                              |
|         "mid": "..."                                               |
|       }                                                           |
+-------------------------------------------------------------------+
```
> **دستورالعمل**: این ورک‌فلو را بسازید، اطلاعات کامل Session JSON خود را در آن قرار دهید و روی "Execute Workflow" کلیک کنید. اگر با موفقیت اجرا شد، شما با موفقیت لاگین کرده‌اید. دیگر نیازی به اجرای مجدد این ورک‌فلو ندارید مگر اینکه نشست شما منقضی شود.

### ورک‌فلو پیشرفته: پاسخ هوشمند و قانون‌مند به کامنت‌ها

این ورک‌فلو:
۱. به صورت زمان‌بندی شده اجرا می‌شود.
۲. آخرین پست‌های اینستاگرام شما را دریافت می‌کند.
۳. برای هر پست، کامنت‌های آن را دریافت می‌کند.
۴. کامنت‌هایی که قبلاً به آن‌ها پاسخ داده‌اید را فیلتر می‌کند.
۵. یک فایل Google Sheet را برای پیدا کردن قوانین منطبق (بر اساس لینک پست، کلمات کلیدی و وضعیت فالو) بررسی می‌کند.
۶. اگر قانونی پیدا شد، پاسخی را که در Google Sheet تعریف شده ارسال می‌کند.
۷. در غیر این صورت، یک پاسخ با استفاده از هوش مصنوعی تولید و ارسال می‌کند.

#### دیاگرام کلی ورک‌فلو

```
[Cron] -> [دریافت پست‌ها] -> [حلقه پست‌ها] -> [دریافت کامنت‌ها] -> [حلقه کامنت‌ها] -> [فیلتر پاسخ‌داده‌شده] -> [خواندن شیت] -> [IF: قانون یافت شد؟]
                                                                                                                      |
                                                                                                  +-------------------+-------------------+
                                                                                                  | (بله)                               | (خیر)
                                                                                                  v                                   v
                                                                           [کد: تطابق کلیدواژه؟] -> [IF: تطابق دارد؟]          [عامل AI]
                                                                                                  |      | (بله)                      |
                                                                                                  |      v                            |
                                                                             (خیر)|      [بررسی فالوور] -> [IF: فالوور است؟]      |
                                                                                                  |      | (بله)         | (خیر)      |
                                                                                                  |      v               v            |
                                                                                                  |   [پاسخ سفارشی]  [پاسخ "فالو کن"]  |
                                                                                                  |      |               |            |
                                                                                                  +------+---------------+------------+
                                                                                                         |
                                                                                                         v
                                                                                                     [ارسال پاسخ AI]
```

#### تنظیمات قدم به قدم نودها

*(این یک راهنمای دقیق است. هر مرحله معادل یک نود در n8n است.)*

**۱. نود Cron: "شروع زمان‌بندی شده"**
*این نود ورک‌فلو را به صورت خودکار آغاز می‌کند.*
```
+-------------------------------------------------------------------+
| [1] نود Cron                                                      |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Mode:           Every X Minutes     (حالت: Fixed)            |
|   Minutes:        15                  (حالت: Fixed)            |
+-------------------------------------------------------------------+
```

**۲. نود HTTP Request: "دریافت آخرین پست‌ها"**
*جدیدترین پست‌های حساب اینستاگرام شما را دریافت می‌کند.*
```
+-------------------------------------------------------------------+
| [2] نود HTTP Request: "دریافت آخرین پست‌ها"                       |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Request Method:    POST               (حالت: Fixed)            |
|   URL:               http://localhost:8000/api/n8n/action (حالت: Fixed) |
|   Body Content Type: JSON               (حالت: Fixed)            |
|   JSON/RAW Parameters:                                            |
|     - کلید: action                   (حالت: Fixed)            |
|     - مقدار: get_user_posts         (حالت: Fixed)            |
|     - کلید: payload                  (حالت: Fixed)            |
|     - مقدار: { "amount": 5 }        (حالت: Fixed)            |
| Options:                                                          |
|   Split Into:     Items               (حalt: Fixed)            |
|   Path:           data                (حالت: Fixed)            |
+-------------------------------------------------------------------+
```

**۳. نود HTTP Request: "دریافت کامنت‌های پست"**
*برای هر پست از مرحله قبل، کامنت‌های آن را دریافت می‌کند.*
```
+-------------------------------------------------------------------+
| [3] نود HTTP Request: "دریافت کامنت‌های پست"                      |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Request Method:    POST               (حالت: Fixed)            |
|   URL:               http://localhost:8000/api/n8n/action (حالت: Fixed) |
|   Body Content Type: JSON               (حالت: Fixed)            |
|   JSON/RAW Parameters:                                            |
|     - کلید: action                   (حالت: Fixed)            |
|     - مقدار: get_media_comments     (حالت: Fixed)            |
|     - کلید: payload                  (حالت: Expression)       |
|     - مقدار: { "media_id": "{{ $json.pk }}" }                   |
| Options:                                                          |
|   Split Into:     Items               (حالت: Fixed)            |
|   Path:           data                (حالت: Fixed)            |
+-------------------------------------------------------------------+
```
> **جریان داده**: `media_id` به صورت پویا از خروجی نود "دریافت آخرین پست‌ها" گرفته می‌شود. `{{ $json.pk }}` به فیلد `pk` هر پست اشاره دارد.

**۴. نود Code: "فیلتر کامنت‌های پاسخ داده شده"**
*این نود ساده بررسی می‌کند که آیا شما قبلاً به یک کامنت پاسخ داده‌اید یا خیر و در این صورت، ادامه ورک‌فلو را برای آن کامنت متوقف می‌کند.*
```
+-------------------------------------------------------------------+
| [4] نود Code: "فیلتر کامنت‌های پاسخ داده شده"                      |
+-------------------------------------------------------------------+
| Language:       JavaScript                                        |
| Code:                                                             |
|   const hasReplied = $json.has_liked; // پراکسی برای پاسخ‌ها       |
|   if (hasReplied) {                                               |
|     return null; // اجرای این آیتم را متوقف کن                    |
|   }                                                               |
|   return $json; // اگر پاسخ نداده بودی، ادامه بده                 |
+-------------------------------------------------------------------+
```

**۵. نود Google Sheets: "خواندن قوانین از شیت"**
*این نود قوانین را از یک فایل اکسل آنلاین می‌خواند.*
> **تنظیمات اولیه**: یک فایل Google Sheet با ستون‌های `PostURL`, `Keywords`, `FollowerOnly`, `CommentReply`, `DMReply` بسازید.

```
+-------------------------------------------------------------------+
| [5] نود Google Sheets: "خواندن قوانین از شیت"                     |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Authentication:    اکانت گوگل خود را متصل کنید                   |
|   Resource:          Row                                          |
|   Operation:         Lookup                                       |
|   Spreadsheet:       فایل شیت خود را انتخاب کنید                   |
|   Sheet:             شیت مورد نظر را انتخاب کنید                   |
|   Column To Match On: PostURL             (حالت: Fixed)            |
|   Value To Match:    {{ "https://www.instagram.com/p/" + $('دریافت کامنت‌های پست').json.code + "/" }} (حالت: Expression) |
+-------------------------------------------------------------------+
```

**۶. نود IF: "قانون یافت شد؟"**
*بررسی می‌کند که آیا نود Google Sheets یک قانون منطبق پیدا کرده است یا خیر.*
```
+-------------------------------------------------------------------+
| [6] نود IF: "قانون یافت شد؟"                                       |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - شرط ۱:                                                        |
|     - مقدار ۱: {{ $('خواندن قوانین از شیت').json.Keywords }} (حالت: Expression)|
|     - عملیات: Is Not Empty (خالی نیست)                             |
+-------------------------------------------------------------------+
```

#### شاخه TRUE (پاسخ بر اساس قانون)

**۷الف. نود Code: "بررسی تطابق کلمات کلیدی"**
*اگر قانونی پیدا شد، این نود بررسی می‌کند که آیا متن کامنت، حاوی یکی از کلمات کلیدی تعریف شده در شیت است یا خیر.*
```
+-------------------------------------------------------------------+
| [7a] نود Code: "بررسی تطابق کلمات کلیدی"                           |
+-------------------------------------------------------------------+
| Language:       JavaScript                                        |
| Code:                                                             |
|   const keywords = $('خواندن قوانین از شیت').json.Keywords.split(','); |
|   const commentText = $('فیلتر کامنت‌های پاسخ داده شده').json.text.toLowerCase(); |
|   const match = keywords.some(k => commentText.includes(k.trim())); |
|   return { ...$item.json, ruleMatched: match };                   |
+-------------------------------------------------------------------+
```

**۸الف. نود IF: "کلمه کلیدی تطابق داشت؟"**
*این نود را به خروجی نود کد قبلی متصل کنید. فقط در صورتی ادامه می‌دهد که `ruleMatched` برابر `true` باشد.*
```
+-------------------------------------------------------------------+
| [8a] نود IF: "کلمه کلیدی تطابق داشت؟"                              |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - شرط ۱:                                                        |
|     - مقدار ۱: {{ $json.ruleMatched }} (حالت: Expression)         |
|     - عملیات: Is True                                             |
+-------------------------------------------------------------------+
```

**۹الف. نود HTTP Request: "بررسی وضعیت فالوور"**
*به خروجی **TRUE** نود "کلمه کلیدی تطابق داشت؟" متصل شود. این نود بررسی می‌کند که آیا کامنت‌گذار شما را فالو می‌کند یا خیر.*
```
+-------------------------------------------------------------------+
| [9a] نود HTTP Request: "بررسی وضعیت فالوور"                       |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Request Method:    POST               (حالت: Fixed)            |
|   URL:               http://localhost:8000/api/n8n/action (حالت: Fixed) |
|   Body Content Type: JSON               (حالت: Fixed)            |
|   Body:                                                           |
|     - action: check_follower_status     (حالت: Fixed)            |
|     - payload: { "target_user_id": "{{ $('فیلتر کامنت‌های پاسخ داده شده').json.user.pk }}" } (حالت: Expression) |
+-------------------------------------------------------------------+
```

**۱۰الف. نود IF: "آیا فالوور است؟"**
*این نود بر اساس وضعیت فالوور و قانون تعریف شده در شیت، تصمیم می‌گیرد کدام پاسخ را ارسال کند.*
```
+-------------------------------------------------------------------+
| [10a] نود IF: "آیا فالوور است؟"                                    |
+-------------------------------------------------------------------+
| Conditions:                                                       |
|   - شرط ۱:                                                        |
|     - مقدار ۱: {{ $('خواندن قوانین از شیت').json.FollowerOnly }} (حالت: Expression)|
|     - عملیات: Is False                                            |
|   - شرط ۲ (OR):                                                   |
|     - مقدار ۱: {{ $('بررسی وضعیت فالوور').json.is_follower }} (حالت: Expression)|
|     - عملیات: Is True                                             |
+-------------------------------------------------------------------+
```

**۱۱الف. نود HTTP Request: "ارسال پاسخ سفارشی"**
*به خروجی **TRUE** نود "آیا فالوور است؟" متصل شود. این نود پاسخ اصلی را ارسال می‌کند.*
```
+-------------------------------------------------------------------+
| [11a] نود HTTP Request: "ارسال پاسخ سفارشی"                       |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('فیلتر کامنت‌های پاسخ داده شده').json.media.pk }}", "text": "{{ $('خواندن قوانین از شیت').json.CommentReply }}" } (حالت: Expression)|
+-------------------------------------------------------------------+
```

**۱۲الف. نود HTTP Request: "ارسال پاسخ لطفا فالو کنید"**
*به خروجی **FALSE** نود "آیا فالوور است؟" متصل شود. این نود پاسخ جایگزین را ارسال می‌کند.*
```
+-------------------------------------------------------------------+
| [12a] نود HTTP Request: "ارسال پاسخ لطفا فالو کنید"               |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('فیلتر کامنت‌های پاسخ داده شده').json.media.pk }}", "text": "برای دریافت پاسخ، لطفا ابتدا پیج ما را فالو کنید!" } (حالت: Expression)|
+-------------------------------------------------------------------+
```

#### شاخه FALSE (پاسخ با هوش مصنوعی)

**۷ب. نود OpenAI: "تولید پاسخ با AI"**
*این نود را به خروجی **FALSE** نود "قانون یافت شد؟" متصل کنید.*
```
+-------------------------------------------------------------------+
| [7b] نود OpenAI: "تولید پاسخ با AI"                               |
+-------------------------------------------------------------------+
| پارامترها:                                                        |
|   Resource:       Chat                                            |
|   Model:          gpt-4o                                          |
|   Prompt:         بر اساس این کامنت: "{{ $('فیلتر کامنت‌های پاسخ داده شده').json.text }}"، یک پاسخ دوستانه و مفید بنویس. |
+-------------------------------------------------------------------+
```

**۸ب. نود HTTP Request: "ارسال پاسخ AI"**
*این نود را به خروجی نود OpenAI متصل کنید.*
```
+-------------------------------------------------------------------+
| [8b] نود HTTP Request: "ارسال پاسخ AI"                            |
+-------------------------------------------------------------------+
|   Body:                                                           |
|     - payload: { "media_id": "{{ $('فیلتر کامنت‌های پاسخ داده شده').json.media.pk }}", "text": "{{ $('تولید پاسخ با AI').json.choices[0].message.content }}" } (حالت: Expression)|
+-------------------------------------------------------------------+
```
