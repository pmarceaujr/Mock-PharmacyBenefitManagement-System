import type { Drug } from "@/types";
import { api } from "./api";

export const drugService = {
    getAll: async (params?: {
        page?: number;
        per_page?: number;
        search?: string;
        is_generic?: boolean;
        therapeutic_class?: string;
    }) => {
        const response = await api.get("/api/drugs", { params });
        return {
            items: response.data.drugs,
            total: response.data.total,
            pages: response.data.pages,
            current_page: response.data.current_page,
        };
    },

    getById: async (id: number) => {
        const response = await api.get<Drug>(`/api/drugs/${id}`);
        return response.data;
    },

    search: async (query: string, limit: number = 10) => {
        const response = await api.get<{ query: string; results: Drug[] }>("/api/drugs/search", {
            params: { q: query, limit },
        });
        return response.data.results;
    },

    create: async (data: Partial<Drug>) => {
        const response = await api.post<Drug>("/api/drugs", data);
        return response.data;
    },

    update: async (id: number, data: Partial<Drug>) => {
        const response = await api.put<Drug>(`/api/drugs/${id}`, data);
        return response.data;
    },
};
