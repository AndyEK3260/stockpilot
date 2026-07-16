from services.score_service import get_stock_score


def build_summary(score_data):

    reasons = score_data["reasons"]

    summary = "，".join(reasons)

    return f"目前技術分析顯示：{summary}。"


def build_risks():

    risks = [

        "尚未納入財報分析",

        "尚未納入法人買賣超",

        "尚未納入估值分析"

    ]

    return risks


def calculate_confidence():

    # 第一版只有 Technical

    return 40


def generate_diagnosis(ticker):

    score = get_stock_score(ticker)

    diagnosis = {

        "ticker": score["ticker"],

        "name": score["name"],

        "overall": {

            "score": score["score"],

            "signal": score["signal"],

            "confidence": calculate_confidence()

        },

        "technical": {

            "score": score["score"],

            "breakdown": score["breakdown"]

        },

        "financial": {

            "status": "NO_DATA"

        },

        "institutional": {

            "status": "NO_DATA"

        },

        "valuation": {

            "status": "NO_DATA"

        },

        "summary": build_summary(score),

        "risks": build_risks()

    }

    return diagnosis
