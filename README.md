# Instagram Automation Tool

An open-source, self-hosted Instagram automation tool similar to ManyChat, designed to run without official API keys. It provides a backend API and a simple frontend interface to manage comment and DM automation tasks.

This project uses `instagrapi` for Instagram communication and can be deployed easily using Docker.

---

## Table of Contents

- [Features](#features)
- [Safety Features & Human-Like Behavior](#safety-features--human-like-behavior)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [API Documentation](#api-documentation)
- [Connecting with n8n (Advanced Tutorial)](#connecting-with-n8n-advanced-tutorial)
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

1.  **Backend (FastAPI)**: A Python server that handles all the logic. It uses the `instagrapi` library to connect to Instagram, listen for comments on specific posts, and perform actions like replying or sending DMs.
2.  **Frontend (Vanilla JS/HTML/CSS)**: A simple user interface that runs in your browser. It communicates with the backend's API to allow you to log in, create, and manage automation tasks.

... (The rest of the README remains the same as the last complete version) ...

---

# Farsi Documentation (مستندات فارسی)

... (The Farsi introduction and other sections remain the same) ...

---
## ویژگی‌های ایمنی و شبیه‌سازی رفتار انسانی

این ابزار با در نظر گرفتن ایمنی حساب اینستاگرام شما طراحی شده است. برای جلوگیری از شناسایی شدن به عنوان ربات و به حداقل رساندن خطر مسدود شدن حساب، قابلیت‌های زیر پیاده‌سازی شده‌اند:

-   **جلوگیری از پاسخ تکراری**: ابزار به کامنتی که قبلاً پاسخ داده شده باشد (چه توسط شما و چه توسط ربات)، دوباره پاسخ نمی‌دهد. این کار با بررسی "لایک" شدن کامنت توسط شما انجام می‌شود (اینستاگرام به صورت خودکار کامنتی را که به آن پاسخ می‌دهید لایک می‌کند).
-   **تأخیرهای تصادفی**: قبل از ارسال هر کامنت یا دایرکت، ربات برای یک مدت زمان تصادفی (بین ۵ تا ۱۵ ثانیه) صبر می‌کند تا رفتار و زمان پاسخ‌دهی انسان را شبیه‌سازی کند.
-   **فواصل زمانی متغیر**: ربات در بازه‌های زمانی متغیر (بین ۶۰ تا ۱۰۰ ثانیه) به جای یک زمان ثابت، کامنت‌های جدید را بررسی می‌کند. این کار الگوی فعالیت آن را کمتر قابل پیش‌بینی می‌کند.
-   **کش بهینه فالوورها**: لیست فالوورهای شما به مدت ۳۰ دقیقه در حافظه موقت (کش) نگهداری می‌شود تا تعداد درخواست‌های ارسالی به سرور اینستاگرام به شدت کاهش یابد، که این عامل کلیدی در جلوگیری از محدودیت‌هاست.

> **سلب مسئولیت**: با وجود اینکه این اقدامات ایمنی را به طور قابل توجهی افزایش می‌دهند، استفاده از هرگونه ابزار اتوماسیون در اینستاگرام با ریسک‌های ذاتی همراه است. لطفاً با مسئولیت از آن استفاده کنید.

... (The rest of the Farsi documentation remains the same) ...
