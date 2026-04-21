from flask import Flask, jsonify
from datetime import datetime
import random
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample horoscope data
HOROSCOPES = {
    "aries": "今天是新的開始，勇敢地追逐你的夢想吧！",
    "taurus": "穩定的一天，適合專注於長期目標和財務規劃。",
    "gemini": "沟通順暢，適合進行社交活動和學習新知識。",
    "cancer": "關注家庭和情感需求，今天適合好好照顧自己。",
    "leo": "你的魅力與創造力達到峰值，是展現自己的好時機。",
    "virgo": "注重細節的一天，工作和學習都會有不錯的進展。",
    "libra": "人際關係和諧，適合處理合作事項和尋求平衡。",
    "scorpio": "深度思考和內省的一天，適合探索內心世界。",
    "sagittarius": "冒險精神高漲，適合計畫旅行或嘗試新事物。",
    "capricorn": "踏實努力會有回報，專注於職涯發展和目標達成。",
    "aquarius": "獨特想法與創意爆發，適合進行創新專案。",
    "pisces": "直覺特別敏銳，適合藝術創作和精神修練。\n"
}

# Weekly horoscope data (static for simplicity)
WEEKLY_HOROSCOPES = {
    "aries": "這週是新機會的週期，勇敢地接受挑戰，你的領導能力將被認可。",
    "taurus": "這週財務方面穩定，適合進行長期投資規劃，人際關係和諧。",
    "gemini": "這週沟通順暢，適合學習新技能和進行社交活動，創意靈感爆發。",
    "cancer": "這週關注家庭和情感需求，適合進行家庭活動和自我照顧，直覺特別敏銳。",
    "leo": "這週你的魅力與創造力達到峰值，是展現自己和進行創意專案的好時機。",
    "virgo": "這週注重細節的一天，工作和學習都會有不錯的進展，適合整理和規劃。",
    "libra": "這週人際關係和諧，適合處理合作事項和尋求平衡，適合進行團隊項目。",
    "scorpio": "這週深度思考和內省的一天，適合探索內心世界和進行精神修練。",
    "sagittarius": "這週冒險精神高漲，適合計畫旅行或嘗試新事物，適合戶外活動和探索。",
    "capricorn": "這週踏實努力會有回報，專注於職涯發展和目標達成，適合進行職涯規劃。",
    "aquarius": "這週獨特想法與創意爆發，適合進行創新專案和科技探索，適合團隊合作。",
    "pisces": "這週直覺特別敏銳，適合藝術創作和精神修練，適合進行藝術和音樂創作。\n"
}

@app.route('/')
def index():
    return jsonify({
        "message": "Stellar Whisper API",
        "version": "1.0.0",
        "endpoints": ["/horoscope/<sign>", "/horoscope/today", "/horoscope/weekly/<sign>", "/horoscope/<sign>/<date>"]
    })

@app.route('/horoscope/<sign>')
def get_horoscope(sign):
    sign = sign.lower()
    if sign in HOROSCOPES:
        return jsonify({
            "sign": sign,
            "horoscope": HOROSCOPES[sign],
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    else:
        return jsonify({"error": "Invalid zodiac sign"}), 400

@app.route('/horoscope/today')
def get_today_horoscopes():
    today = datetime.now().strftime("%Y-%m-%d")
    horoscopes = []
    for sign, text in HOROSCOPES.items():
        horoscopes.append({
            "sign": sign,
            "horoscope": text,
            "date": today
        })
    return jsonify({
        "date": today,
        "horoscopes": horoscopes
    })

@app.route('/horoscope/weekly/<sign>')
def get_weekly_horoscope(sign):
    sign = sign.lower()
    if sign in WEEKLY_HOROSCOPES:
        return jsonify({
            "sign": sign,
            "horoscope": WEEKLY_HOROSCOPES[sign],
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    else:
        return jsonify({"error": "Invalid zodiac sign"}), 400

@app.route('/horoscope/<sign>/<date>')
def get_horoscope_specific_date(sign, date):
    sign = sign.lower()
    # Validate the sign
    if sign not in HOROSCOPES:
        return jsonify({"error": "Invalid zodiac sign"}), 400
    # Validate the date format (YYYY-MM-DD)
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    return jsonify({
        "sign": sign,
        "horoscope": HOROSCOPES[sign],
        "date": date
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)