from services.scoring_service import calculate_investment_score

from services.score_history_service import save_stock_score



score = calculate_investment_score(

    2439,

    2419.5,

    2299.5,

    52.6044,

    33.7927

)


print(score)



save_stock_score(

    "2330",

    score

)