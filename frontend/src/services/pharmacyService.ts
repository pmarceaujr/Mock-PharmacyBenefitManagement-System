import type { Pharmacy } from "@/types";
import { api } from "./api";

export const pharmacyService = {
    getAll: async (params?: {
        page?: number;
        per_page?: number;
        search?: string;
        city?: string;
        state?: string;
        in_network?: boolean;
    }) => {
        const response = await api.get("/api/pharmacies", { params });
        return {
            items: response.data.pharmacies,
            total: response.data.total,
            pages: response.data.pages,
            current_page: response.data.current_page,
        };
    },

    getById: async (id: number) => {
        const response = await api.get<Pharmacy>(`/api/pharmacies/${id}`);
        return response.data;
    },

    create: async (data: Partial<Pharmacy>) => {
        const response = await api.post<Pharmacy>("/api/pharmacies", data);
        return response.data;
    },

    update: async (id: number, data: Partial<Pharmacy>) => {
        const response = await api.put<Pharmacy>(`/api/pharmacies/${id}`, data);
        return response.data;
    },
};
