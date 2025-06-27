# fin-sender

> **Upload a `.fin` file** as a binary blob to the BRI endpoint using Docker, with real-time status notifications via Telegram.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Project Structure](#-project-structure)
3. [Prerequisites](#-prerequisites)
4. [Environment Configuration](#-environment-configuration)
5. [Build & Run](#-build--run)
6. [Logging & Notifications](#-logging--notifications)
7. [Branching & Contribution](#-branching--contribution)
8. [License](#-license)

---

## 🚀 Features

* Display the container’s **public IP** before sending requests.
* OAuth2 authentication (client\_credentials grant).
* Upload `.fin` files as `application/octet-stream`.
* Real-time status updates in both terminal and Telegram.

---

## 📂 Project Structure

```
fin-sender/
├── send_fin.py           # Main script (OAuth token + file upload)
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Compose setup with environment variables
├── .env.example          # Sample environment variable file
└── data/
    └── in/               # Mounted directory for .fin files (read-only)
```

---

## 🔧 Prerequisites

1. **Clone the repository**:

   ```bash
   git clone https://github.com/username/fin-sender.git
   cd fin-sender
   ```
2. **Copy the example env file**:

   ```bash
   cp .env.example .env
   ```
3. **Edit `.env`** according to your credentials and file path.

---

## ⚙️ Environment Configuration

Create and update `.env` in the project root:

```dotenv
# BRI API settings
BRI_BASE_URL=your-endpoint
BRI_CLIENT_ID=your-client-id
BRI_CLIENT_SECRET=your-client-secret

# Target .fin file path inside container
FILENAME=/in/yourfile.fin

# Telegram notifications
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Optional: HTTP/HTTPS proxy
# HTTP_PROXY=http://user:pass@host:port
# HTTPS_PROXY=http://user:pass@host:port
```

---

## 🏗️ Build & Run

1. **Build the Docker image**:

   ```bash
   docker compose build
   ```
2. **Run the uploader**:

   ```bash
   docker compose run --rm sender
   ```

> Logs will print to the terminal, and Telegram notifications will be sent if configured.

---

## 📈 Logging & Notifications

* **Public IP**: Shown at startup.
* **OAuth**: Prints status code and response snippet.
* **Upload**: Prints status code and response snippet.
* **Errors**: Clear error messages (e.g. `wrong URL OAuth`).

---

## 🌱 Branching & Contribution

* Default branch: `main`.
* Fork and create feature/bugfix branches.
* Submit pull requests with detailed change descriptions.

---

## ⚖️ License

Distributed under the MIT License. © 2025
