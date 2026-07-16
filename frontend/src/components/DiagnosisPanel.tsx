interface DiagnosisProps {
    diagnosis: {
        summary: string;

        financial: {
            status: string;
        };

        institutional: {
            status: string;
        };

        valuation: {
            status: string;
        };
    };
}

export default function DiagnosisPanel({ diagnosis }: DiagnosisProps) {
    return (
        <div className="card">
            <h2>AI Diagnosis</h2>

            <p>{diagnosis.summary}</p>

            <hr />

            <p>Financial : {diagnosis.financial.status}</p>

            <p>Institutional : {diagnosis.institutional.status}</p>

            <p>Valuation : {diagnosis.valuation.status}</p>
        </div>
    );
}