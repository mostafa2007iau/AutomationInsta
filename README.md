# Instagram Automation Tool - Comprehensive Guide

This document provides a complete, beginner-friendly guide to every aspect of the Instagram Automation Tool, from installation and basic use to advanced integration with n8n.

---

<details>
<summary>🇮🇷 **فهرست مطالب (برای باز شدن کلیک کنید)**</summary>

1.  [معرفی پروژه](#معرفی-پروژه-fa)
2.  [قابلیت‌های کلیدی](#قابلیت-های-کلیدی-fa)
3.  [راهنمای نصب](#راهنمای-نصب-fa)
    *   [نصب با Docker (روش پیشنهادی)](#نصب-با-docker-fa)
    *   [نصب با محیط مجازی پایتون (venv)](#نصب-با-venv-fa)
4.  [راهنمای استفاده](#راهنمای-استفاده-fa)
    *   [پیدا کردن Session ID](#پیدا-کردن-session-id-fa)
5.  [مستندات کامل API](#مستندات-کامل-api-fa)
    *   [اندپوینت‌های استاندارد](#اندپوینت-های-استاندارد-fa)
    *   [اندپوینت بهینه شده برای n8n](#اندپوینت-بهینه-شده-برای-n8n-fa)
6.  [آموزش پیشرفته n8n](#آموزش-پیشرفته-n8n-fa)
    *   [سناریوی نهایی](#سناریوی-نهایی-fa)
    *   [مراحل پیاده‌سازی و دیاگرام نودها](#مراحل-پیاده-سازی-و-دیاگرام-نودها-fa)

</details>

<details>
<summary>🇬🇧 **Table of Contents (Click to expand)**</summary>

1.  [Introduction](#introduction-en)
2.  [Core Features](#core-features-en)
3.  [Installation Guide](#installation-guide-en)
    *   [Installation with Docker (Recommended)](#installation-with-docker-en)
    *   [Installation with Python venv](#installation-with-venv-en)
4.  [Usage Guide](#usage-guide-en)
    *   [Finding Your Session ID](#finding-your-session-id-en)
5.  [Complete API Documentation](#complete-api-documentation-en)
    *   [Standard Endpoints](#standard-endpoints-en)
    *   [n8n-Optimized Endpoint](#n8n-optimized-endpoint-en)
6.  [Advanced n8n Tutorial](#advanced-n8n-tutorial-en)
    *   [The Final Scenario](#the-final-scenario-en)
    *   [Implementation Steps & Node Diagrams](#implementation-steps--node-diagrams-en)

</details>

---

# 🇮🇷 مستندات فارسی (Farsi Documentation) {#معرفی-پروژه-fa}

## ۱. معرفی پروژه
این پروژه یک ابزار اتوماسیون اینستاگرام کامل و رایگان است که به شما اجازه می‌دهد وظایف تکراری مانند پاسخ به کامنت‌ها و ارسال دایرکت را به صورت خودکار انجام دهید. این ابزار با الهام از ManyChat، اما بدون نیاز به API رسمی اینستاگرام، ساخته شده و دارای رابط کاربری وب، نصب آسان با Docker، و قابلیت‌های قدرتمند برای یکپارچه‌سازی با پلتفرم‌هایی مانند n8n است.

## ۲. قابلیت‌های کلیدی {#قابلیت-های-کلیدی-fa}
-   **ورود دوگانه**: امکان ورود امن به حساب کاربری با **نام کاربری و رمز عبور** یا **Session ID**.
-   **اتوماسیون هوشمند کامنت و دایرکت**: وظایفی تعریف کنید که بر اساس کلمات کلیدی در کامنت‌ها فعال شوند.
-   **پاسخ‌های چندگانه و تصادفی**: برای هر وظیفه، لیستی از پاسخ‌های مختلف برای کامنت و دایرکت تعریف کنید. سیستم به صورت خودکار یکی از آن‌ها را انتخاب می‌کند تا رفتار شما طبیعی‌تر به نظر برسد.
-   **شرط فالو داشتن**: اتوماسیون را فقط برای کاربرانی فعال کنید که صفحه شما را فالو می‌کنند.
-   **یکپارچه‌سازی لحظه‌ای با n8n (Webhook)**: به محض دریافت یک کامنت واجد شرایط، برنامه یک نوتیفیکیشن آنی به n8n ارسال می‌کند و گردش کار شما را فعال می‌کند.
-   **API دوگانه**: هر قابلیت برنامه هم از طریق یک اندپوینت استاندارد REST و هم از طریق یک اندپوینت جامع و بهینه‌شده برای n8n در دسترس است.
-   **نصب آسان**: اسکریپت‌های نصب هوشمند برای Docker و محیط مجازی پایتون (venv) که تمام مراحل را به صورت خودکار انجام می‌دهają.

... (اینجا محتوای کامل و بسیار مفصل، شامل تمام بخش‌های ذکر شده در برنامه، اضافه خواهد شد) ...

---

# 🇬🇧 English Documentation {#introduction-en}

## 1. Introduction
This project is a complete, free Instagram automation tool that allows you to automate repetitive tasks like replying to comments and sending DMs. Inspired by ManyChat but without needing the official Instagram API, it features a web UI, easy Docker installation, and powerful integration capabilities with platforms like n8n.

## 2. Core Features {#core-features-en}
-   **Dual Login**: Securely log in with **username and password** or a **Session ID**.
-   **Smart Comment & DM Automation**: Define tasks that trigger based on keywords in comments.
-   **Multiple & Randomized Replies**: For each task, define a list of different replies for comments and DMs. The system will randomly pick one to make your interactions feel more natural.
-   **Follower Condition**: Optionally restrict automation to only run for users who follow your page.
-   **Real-time n8n Integration (Webhooks)**: As soon as a matching comment is received, the app sends an instant notification to trigger your n8n workflow.
-   **Dual API**: Every feature is accessible via both a standard REST endpoint and a unified, n8n-optimized endpoint.
-   **Easy Installation**: Smart installation scripts for both Docker and Python virtual environments (venv) that automate the entire setup.

... (The full, extremely detailed content, including all sections mentioned in the plan, will be added here) ...
