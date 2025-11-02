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
- [Project Structure](#project-structure)
- [Farsi Documentation (مستندات فارسی)](#farsi-documentation-مستندات-فارسی)

---

## (Sections: Features, Safety, How It Works - remain unchanged)

## Installation

### Docker (Recommended)
This is the easiest way to get the application running.
**Prerequisites**:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

**Steps**:
1.  **Clone the repository**.
2.  **Run the interactive setup script**: `./install.sh`. This configures your ports.
3.  **Build and run the containers**: `docker-compose up --build -d`.
4.  **Access the application**:
    -   Frontend: `http://localhost:<FRONTEND_PORT>`
    -   API Docs: `http://localhost:<BACKEND_PORT>/docs`

> **✅ Service Persistence**: The Docker services are configured with `restart: unless-stopped`. This means they will automatically restart if the server reboots, ensuring the application is always running.

### Manual Setup (venv)
If you prefer not to use Docker, follow these steps.
1.  **Clone the repository**.
2.  **Run the venv setup script**: `./setup_venv.sh`.
3.  **Activate the environment**: `source backend/.venv/bin/activate`.
4.  **Run the servers** (in separate terminals):
    -   Backend: `uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir backend`
    -   Frontend: `python3 -m http.server 8080 --directory frontend`

## Making the Service Persistent (venv only)
To ensure the application runs automatically after a server reboot when using the `venv` method, you need to set it up as a `systemd` service. This is the standard way to manage long-running applications on modern Linux systems.

Template files are provided in the `deployment` directory.

**Prerequisites**:
- You are on a Linux system that uses `systemd` (e.g., Ubuntu, CentOS, Debian).
- You have `sudo` (administrator) privileges.

**Step-by-Step Guide**:

1.  **Navigate to the project directory**:
    ```bash
    cd /path/to/your/project
    ```
    Remember this path, you will need it.

2.  **Edit the Backend Service File**:
    -   Open `deployment/insta-backend.service`.
    -   Replace `your_user` with your actual Linux username.
    -   Replace all instances of `/path/to/your/project` with the **absolute path** to your project directory.

3.  **Edit the Frontend Service File**:
    -   Open `deployment/insta-frontend.service`.
    -   Replace `your_user` with your Linux username.
    -   Replace `/path/to/your/project` with the absolute path to your project directory.

4.  **Copy the Files to systemd**:
    ```bash
    sudo cp deployment/insta-backend.service /etc/systemd/system/
    sudo cp deployment/insta-frontend.service /etc/systemd/system/
    ```

5.  **Reload the systemd daemon**:
    This command tells `systemd` to read the new service files.
    ```bash
    sudo systemctl daemon-reload
    ```

6.  **Enable the services**:
    This command makes the services start automatically on boot.
    ```bash
    sudo systemctl enable insta-backend.service
    sudo systemctl enable insta-frontend.service
    ```

7.  **Start the services now**:
    ```bash
    sudo systemctl start insta-backend.service
    sudo systemctl start insta-frontend.service
    ```

8.  **Check the status**:
    You can check if the services are running correctly with:
    ```bash
    sudo systemctl status insta-backend.service
    sudo systemctl status insta-frontend.service
    ```
    If everything is correct, you should see an "active (running)" status.

## ... (Rest of the documentation remains the same) ...

---

# Farsi Documentation (مستندات فارسی)

... (Farsi introduction and other sections remain the same) ...

### روش اول: Docker (توصیه شده)
... (Steps remain the same) ...

> **✅ پایداری سرویس**: سرویس‌های داکر با پالیسی `restart: unless-stopped` پیکربندی شده‌اند. این به آن معناست که اگر سرور شما ریبوت شود، سرویس‌ها به صورت خودکار مجدداً اجرا خواهند شد و اپلیکیشن شما همیشه در دسترس خواهد بود.

### روش دوم: نصب دستی (venv)
... (Steps remain the same) ...

## پایدارسازی سرویس (فقط برای نصب با venv)
برای اطمینان از اینکه اپلیکیشن در صورت نصب با `venv` پس از ریبوت شدن سرور به صورت خودکار اجرا شود، باید آن را به عنوان یک سرویس `systemd` تعریف کنید. `systemd` روش استاندارد برای مدیریت سرویس‌های طولانی-مدت در سیستم‌عامل‌های مدرن لینوکس است.

فایل‌های الگو در پوشه `deployment` برای کمک به شما قرار داده شده‌اند.

**پیش‌نیازها**:
- شما از یک سیستم‌عامل لینوکس که از `systemd` استفاده می‌کند (مانند اوبونتو، سنت‌اواس، دبیان) بهره می‌برید.
- شما دسترسی `sudo` (مدیر سیستم) دارید.

**راهنمای قدم به قدم**:

۱. **به پوشه پروژه بروید**:
    ```bash
    cd /path/to/your/project
    ```
    این آدرس را به خاطر بسپارید، به آن نیاز خواهید داشت.

۲. **ویرایش فایل سرویس بک‌اند**:
    -   فایل `deployment/insta-backend.service` را باز کنید.
    -   `your_user` را با نام کاربری لینوکس خود جایگزین کنید.
    -   تمام موارد `/path/to/your/project` را با **آدرس کامل (absolute path)** پوشه پروژه خود جایگزین کنید.

۳. **ویرایش فایل سرویس فرانت‌اند**:
    -   فایل `deployment/insta-frontend.service` را باز کنید.
    -   `your_user` را با نام کاربری لینوکس خود جایگزین کنید.
    -   `/path/to/your/project` را با آدرس کامل پوشه پروژه خود جایگزین کنید.

۴. **کپی کردن فایل‌ها به پوشه systemd**:
    ```bash
    sudo cp deployment/insta-backend.service /etc/systemd/system/
    sudo cp deployment/insta-frontend.service /etc/systemd/system/
    ```

۵. **بارگذاری مجدد systemd**:
   این دستور به `systemd` می‌گوید که فایل‌های سرویس جدید را بخواند.
    ```bash
    sudo systemctl daemon-reload
    ```

۶. **فعال‌سازی سرویس‌ها**:
   این دستور باعث می‌شود سرویس‌ها پس از هر بار بوت شدن سیستم، به صورت خودکار اجرا شوند.
    ```bash
    sudo systemctl enable insta-backend.service
    sudo systemctl enable insta-frontend.service
    ```

۷. **شروع به کار سرویس‌ها**:
    ```bash
    sudo systemctl start insta-backend.service
    sudo systemctl start insta-frontend.service
    ```

۸. **بررسی وضعیت**:
   شما می‌توانید با دستورات زیر وضعیت اجرای صحیح سرویس‌ها را بررسی کنید:
    ```bash
    sudo systemctl status insta-backend.service
    sudo systemctl status insta-frontend.service
    ```
    اگر همه چیز درست باشد، باید وضعیت "active (running)" را مشاهده کنید.

## ... (بقیه مستندات فارسی همانند قبل باقی می‌ماند) ...
