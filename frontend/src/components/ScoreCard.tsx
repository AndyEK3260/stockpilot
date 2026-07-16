interface ScoreCardProps {
    score: {
        score: number;
        signal: string;

        breakdown: {
            trend_score: number;
            momentum_score: number;
            macd_score: number;
            risk_score: number;
        };
    };
}

export default function ScoreCard({ score }: ScoreCardProps) {
    return (
        <div className="card">
            <h2>Investment Score</h2>

            <h1>{score.signal}</h1>

            <h3>{score.score}/100</h3>

            <hr />

            <p>Trend: {score.breakdown.trend_score}</p>
            <p>Momentum: {score.breakdown.momentum_score}</p>
            <p>MACD: {score.breakdown.macd_score}</p>
            <p>Risk: {score.breakdown.risk_score}</p>
        </div>
    );
}