interface TechnicalProps {
    technical: {
        MA_5: number;
        MA_20: number;
        MA_60: number;
        RSI_14: number;
        MACD: number;
    };
}

export default function TechnicalChart({ technical }: TechnicalProps) {
    return (
        <div className="card">
            <h2>Technical Analysis</h2>

            <p>MA5 : {technical.MA_5}</p>

            <p>MA20 : {technical.MA_20}</p>

            <p>MA60 : {technical.MA_60}</p>

            <p>RSI : {technical.RSI_14}</p>

            <p>MACD : {technical.MACD}</p>
        </div>
    );
}