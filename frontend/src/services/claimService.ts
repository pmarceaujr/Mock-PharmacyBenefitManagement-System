import type { Claim } from "@/types";
import { api } from "./api";

export const claimService = {
    getAll: async (params?: {
        page?: number;
        per_page?: number;
        status?: string;
        member_id?: number;
        start_date?: string;
        end_date?: string;
    }) => {
        const response = await api.get("/api/claims", { params });
        return {
            items: response.data.claims,
            total: response.data.total,
            pages: response.data.pages,
            current_page: response.data.current_page,
        };
    },

    getById: async (id: number) => {
        const response = await api.get<Claim>(`/api/claims/${id}`);
        return response.data;
    },

    create: async (data: Partial<Claim>) => {
        const response = await api.post<Claim>("/api/claims", data);
        return response.data;
    },

    update: async (id: number, data: Partial<Claim>) => {
        const response = await api.put<Claim>(`/api/claims/${id}`, data);
        return response.data;
    },

    updateStatus: async (id: number, status: string) => {
        const response = await api.put<Claim>(`/api/claims/${id}`, { status });
        return response.data;
    },

    delete: async (id: number) => {
        await api.delete(`/api/claims/${id}`);
    },
};
