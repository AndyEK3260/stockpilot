import { api } from "../api/api";

export async function getStock(ticker: string) {
    const res = await api.get(`/stocks/${ticker}`);
    return res.data;
}

export async function getAnalysis(ticker: string) {
    const res = await api.get(`/stocks/${ticker}/analysis`);
    return res.data;
}

export async function getScore(ticker: string) {
    const res = await api.get(`/stocks/${ticker}/score`);
    return res.data;
}

export async function getDiagnosis(ticker: string) {
    const res = await api.get(`/stocks/${ticker}/diagnosis`);
    return res.data;
}