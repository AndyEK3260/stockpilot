TW_SYMBOLS = {
    "2330": {
        "name_zh": "台積電",
        "market": "TWSE"
    },
    "2317": {
        "name_zh": "鴻海",
        "market": "TWSE"
    }
}


def get_symbol_info(ticker):

    return TW_SYMBOLS.get(ticker)