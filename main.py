from flask import Flask, jsonify
import requests

# 🔹 Notion API-instellingen
NOTION_API_KEY = "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"  # Vervang dit met jouw echte Notion API-key
DATABASES = {
    "SB_Taken": "1b3fd250673d8134ba60f3628c58b5d3",
    "SB_PARA": "1b3fd250673d810292a8da22b6c27143",
    "SB_Notities": "1b3fd250673d81b4a36ffdcc046ef84d",
    "SB_Content": "1b3fd250673d8186b054fbb2e64b9c6c",
    "SB_Daily Pages": "1b3fd250673d8197804ed3437d14c185"
}

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

app = Flask(__name__)

# ✅ **Nieuwe root route**
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Notion API Server is live!"}), 200

# ✅ **Gezondheidscheck**
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ✅ **Route voor ophalen van Notion-data**
@app.route("/notion/<database_name>", methods=["GET"])
def get_notion_data(database_name):
    if database_name not in DATABASES:
        return jsonify({"error": "Database niet gevonden"}), 404

    database_id = DATABASES[database_name]
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Fout bij ophalen van data", "status": response.status_code, "details": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
