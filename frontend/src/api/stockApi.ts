import { api } from "../api/api";   // ✅ 對

export const getStock = async (ticker: string) => {
    const { data } = await api.get(`/stocks/${ticker}`);
    return data;
};

export const getAnalysis = async (ticker: string) => {
    const { data } = await api.get(`/stocks/${ticker}/analysis`);
    return data;
};

export const getScore = async (ticker: string) => {
    const { data } = await api.get(`/stocks/${ticker}/score`);
    return data;
};

export const getDiagnosis = async (ticker: string) => {
    const { data } = await api.get(`/stocks/${ticker}/diagnosis`);
    return data;
};