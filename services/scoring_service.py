from config.diagnosis_rules import (
    MA_BULLISH_SCORE,
    MA_BEARISH_SCORE,
    RSI_HEALTHY_SCORE,
    RSI_OVERBOUGHT_SCORE,
    RSI_OVERSOLD_SCORE,
    MACD_POSITIVE_SCORE,
    MACD_NEGATIVE_SCORE,
    DEFAULT_RISK_SCORE,
    STRONG_BUY_SCORE,
    BUY_SCORE,
    HOLD_SCORE,
    SELL_SCORE
)

# 這些門檻數字本身不在 config/diagnosis_rules.py 裡（該檔案只定義「分數」，
# 沒有定義 RSI 要在什麼區間才算超賣/健康/超買），所以先保留在這裡。
# 如果之後想讓這些也可設定，可以再加進 diagnosis_rules.py。
RSI_OVERSOLD_THRESHOLD = 30
RSI_HEALTHY_LOWER = 40
RSI_HEALTHY_UPPER = 65
RSI_OVERBOUGHT_THRESHOLD = 70


def calculate_investment_score(
    ma5,
    ma20,
    ma60,
    rsi,
    macd
):

    reasons = []

    breakdown = {
        "trend_score": 0,
        "momentum_score": 0,
        "macd_score": 0,
        "risk_score": 0
    }

    # ======================
    # 1. 趨勢評分 MA
    # ======================
    #
    # ⚠️ config/diagnosis_rules.py 只提供兩檔：MA_BULLISH_SCORE / MA_BEARISH_SCORE，
    # 不像上一版有「完整多頭排列 / 短期偏多 / 其他」三檔。
    # 這裡把「ma5 > ma20 但未形成完整多頭排列」也歸類到 MA_BEARISH_SCORE，
    # 只在 reason 文字上做區分。如果你想保留三檔評分，
    # 需要在 diagnosis_rules.py 裡再加一個常數（例如 MA_PARTIAL_SCORE）。

    if ma5 > ma20 > ma60:

        breakdown["trend_score"] = MA_BULLISH_SCORE
        reasons.append("MA多頭排列")

    elif ma5 > ma20:

        breakdown["trend_score"] = MA_BEARISH_SCORE
        reasons.append("短期趨勢偏多，但未形成完整多頭排列")

    else:

        breakdown["trend_score"] = MA_BEARISH_SCORE
        reasons.append("MA呈現空頭或盤整")

    # ======================
    # 2. RSI 動能
    # ======================

    if rsi < RSI_OVERSOLD_THRESHOLD:

        breakdown["momentum_score"] = RSI_OVERSOLD_SCORE
        reasons.append("RSI超賣，可能反彈")

    elif RSI_HEALTHY_LOWER <= rsi <= RSI_HEALTHY_UPPER:

        breakdown["momentum_score"] = RSI_HEALTHY_SCORE
        reasons.append("RSI處於健康區間")

    elif rsi > RSI_OVERBOUGHT_THRESHOLD:

        # ⚠️ 上一版這裡是扣分（-10）。新的 config 裡
        # RSI_OVERBOUGHT_SCORE = 10 是正數，且跟其他 *_SCORE 常數
        # 命名方式一致，所以這裡當成「加分」處理，不再自動取負號。
        # 如果你的本意其實是「超買要扣分」，把下面這行改成
        # `-RSI_OVERBOUGHT_SCORE` 即可。
        breakdown["momentum_score"] = RSI_OVERBOUGHT_SCORE
        reasons.append("RSI過熱")

    # ======================
    # 3. MACD 趨勢
    # ======================

    if macd > 0:

        breakdown["macd_score"] = MACD_POSITIVE_SCORE
        reasons.append("MACD維持正值")

    else:

        breakdown["macd_score"] = -MACD_NEGATIVE_SCORE
        reasons.append("MACD偏弱")

    # ======================
    # 4. 基本風險分
    # ======================

    breakdown["risk_score"] = DEFAULT_RISK_SCORE

    score = sum(breakdown.values())

    # 限制範圍

    score = max(0, min(score, 100))

    # ======================
    # 5. 總分 -> 訊號
    # ======================
    #
    # ⚠️ config 裡有 4 個門檻常數（STRONG_BUY/BUY/HOLD/SELL_SCORE），
    # 但系統目前只有 4 種訊號（STRONG_BUY/BUY/HOLD/SELL）。
    # 所以 SELL_SCORE 目前只當作「SELL」的下限，低於它也還是回傳 SELL，
    # 沒有再往下的第 5 種訊號。如果你想要例如 STRONG_SELL，
    # 跟我說一聲我再加。

    if score >= STRONG_BUY_SCORE:

        signal = "STRONG_BUY"

    elif score >= BUY_SCORE:

        signal = "BUY"

    elif score >= HOLD_SCORE:

        signal = "HOLD"

    elif score >= SELL_SCORE:

        signal = "SELL"

    else:

        signal = "SELL"

    return {
        "score": score,
        "signal": signal,
        "breakdown": breakdown,
        "reasons": reasons
    }