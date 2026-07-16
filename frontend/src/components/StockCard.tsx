interface StockCardProps {
    stock: {
        ticker: string;
        name: string;
        latest_price: number;
        date: string;
    };
}

export default function StockCard({ stock }: StockCardProps) {
    return (
        <div className="card">
            <h2>
                {stock.name} ({stock.ticker})
            </h2>

            <h1>{stock.latest_price}</h1>

            <p>{stock.date}</p>
        </div>
    );
}