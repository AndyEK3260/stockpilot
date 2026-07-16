interface RiskProps {
    risks: string[];
}

export default function RiskPanel({ risks }: RiskProps) {
    return (
        <div className="card">
            <h2>Risk Warning</h2>

            <ul>
                {risks.map((risk, index) => (
                    <li key={index}>{risk}</li>
                ))}
            </ul>
        </div>
    );
}