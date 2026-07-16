"""
Diagnosis Rule Configuration

所有投資規則都集中管理。

未來若想修改權重、買賣門檻，
只需要修改這個檔案，
不用修改任何程式。
"""

# -------------------------
# Engine Weight
# -------------------------

TECHNICAL_WEIGHT = 1.0
FINANCIAL_WEIGHT = 0.0
INSTITUTIONAL_WEIGHT = 0.0
VALUATION_WEIGHT = 0.0


# -------------------------
# Overall Score
# -------------------------

STRONG_BUY_SCORE = 80
BUY_SCORE = 70
HOLD_SCORE = 50
SELL_SCORE = 30


# -------------------------
# Trend Rule
# -------------------------

MA_BULLISH_SCORE = 30
MA_BEARISH_SCORE = 10


# -------------------------
# RSI Rule
# -------------------------

RSI_HEALTHY_SCORE = 20
RSI_OVERBOUGHT_SCORE = 10
RSI_OVERSOLD_SCORE = 15


# -------------------------
# MACD Rule
# -------------------------

MACD_POSITIVE_SCORE = 20
MACD_NEGATIVE_SCORE = 5


# -------------------------
# Risk Rule
# -------------------------

DEFAULT_RISK_SCORE = 10


# -------------------------
# Confidence
# -------------------------

TECHNICAL_CONFIDENCE = 40
FINANCIAL_CONFIDENCE = 30
INSTITUTIONAL_CONFIDENCE = 20
VALUATION_CONFIDENCE = 10