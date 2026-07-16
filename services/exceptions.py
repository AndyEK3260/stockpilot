class StockPilotError(Exception):
    """所有 StockPilot service 層例外的共同基底類別"""
    pass


class CompanyNotFoundError(StockPilotError):
    """指定的 ticker 在 companies 資料表中不存在"""
    pass


class ScoreNotFoundError(StockPilotError):
    """指定的 ticker 目前沒有任何評分資料（尚未跑過批次評分）"""
    pass
