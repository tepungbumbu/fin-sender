#!/usr/bin/env python3
import os
import sys
import socket
import requests
from requests.auth import HTTPBasicAuth

# Environment variables
BASE_URL      = os.getenv("BRI_BASE_URL")
CLIENT_ID     = os.getenv("BRI_CLIENT_ID")
CLIENT_SECRET = os.getenv("BRI_CLIENT_SECRET")
FILENAME      = os.getenv("FILENAME")
TG_TOKEN      = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID    = os.getenv("TELEGRAM_CHAT_ID")

def notify(msg):
    """Cetak ke terminal dan kirim ke Telegram (jika tersedia)."""
    print(f"[NOTIFY] {msg}")
    if TG_TOKEN and TG_CHAT_ID:
        try:
            tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            requests.get(tg_url, params={"chat_id": TG_CHAT_ID, "text": msg}, timeout=5)
        except Exception as e:
            print(f"[NOTIFY][Telegram] Gagal kirim: {e}")

def get_my_public_ip():
    """Ambil IP publik dari api.ipify.org."""
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return "gagal ambil IP publik"

def get_token():
    """Request OAuth token, debug dan validasi JSON."""
    url = f"{BASE_URL}/oauth/client_credential/accesstoken?grant_type=client_credentials"
    r = requests.post(url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), timeout=10)
    print(f"→ [OAuth] status code: {r.status_code}")
    print(f"→ [OAuth] response body:\n{r.text[:200]}...\n")

    content_type = r.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise ValueError(f"wrong URL OAuth: {BASE_URL}")

    r.raise_for_status()
    data = r.json()
    token = data.get("access_token")
    if not token:
        raise ValueError("access_token not found in OAuth response")
    return token

def send_fin(token):
    """Upload file .fin sebagai blob, debug response."""
    if not os.path.isfile(FILENAME):
        raise FileNotFoundError(f"File tidak ditemukan: {FILENAME}")
    with open(FILENAME, "rb") as f:
        blob = f.read()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    r = requests.post(BASE_URL, headers=headers, data=blob, timeout=30)
    print(f"→ [Upload] status code: {r.status_code}")
    print(f"→ [Upload] response body:\n{r.text[:200]}...\n")
    r.raise_for_status()
    return r.json()

def main():
    # Tampilkan IP publik sebelum memulai
    public_ip = get_my_public_ip()
    notify(f"🌐 IP pengirim: {public_ip}")

    try:
        notify("🔑 Mulai request OAuth token…")
        token = get_token()

        notify(f"📤 Mulai upload {FILENAME} ke BRI…")
        res = send_fin(token)

        notify(f"✅ Transfer SUCCESS: {res}")
    except Exception as e:
        notify(f"❌ Transfer FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
