import { useEffect, useState } from "react";

import StockCard from "../components/StockCard";
import ScoreCard from "../components/ScoreCard";
import TechnicalChart from "../components/TechnicalChart";
import DiagnosisPanel from "../components/DiagnosisPanel";
import RiskPanel from "../components/RiskPanel";

import {
    getStock,
    getAnalysis,
    getScore,
    getDiagnosis
} from "../services/stockService";

export default function Home() {

    const [stock, setStock] = useState<any>(null);
    const [analysis, setAnalysis] = useState<any>(null);
    const [score, setScore] = useState<any>(null);
    const [diagnosis, setDiagnosis] = useState<any>(null);

    useEffect(() => {

        async function load() {

            try {

                const stockData = await getStock("2330");
                const analysisData = await getAnalysis("2330");
                const scoreData = await getScore("2330");
                const diagnosisData = await getDiagnosis("2330");

                console.log("Stock =", stockData);
                console.log("Analysis =", analysisData);
                console.log("Score =", scoreData);
                console.log("Diagnosis =", diagnosisData);

                setStock(stockData);
                setAnalysis(analysisData);
                setScore(scoreData);
                setDiagnosis(diagnosisData);

            } catch (err) {
                console.error(err);
            }

        }

        load();

    }, []);

    if (!stock || !analysis || !score || !diagnosis) {
        return <h2>Loading...</h2>;
    }

    return (

        <div
            style={{
                maxWidth: "1100px",
                margin: "0 auto",
                padding: "20px"
            }}
        >

            <StockCard
                stock={{
                    ticker: stock.ticker,
                    name: stock.name,

                    latest_price:
                        stock.market?.latest_price ??
                        stock.latest_price ??
                        0,

                    date:
                        stock.market?.trade_date ??
                        stock.trade_date ??
                        stock.date ??
                        "-"
                }}
            />

            <ScoreCard score={score} />

            <TechnicalChart
                technical={
                    analysis.technical ??
                    analysis
                }
            />

            <DiagnosisPanel
                diagnosis={diagnosis}
            />

            <RiskPanel
                risks={
                    diagnosis.risks ?? []
                }
            />

        </div>

    );

}