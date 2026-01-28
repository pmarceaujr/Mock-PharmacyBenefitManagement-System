import type { Member, PaginatedResponse } from "@/types";
import { api } from "./api";

export const memberService = {
    getAll: async (params?: { page?: number; per_page?: number; search?: string; is_active?: boolean }) => {
        const response = await api.get<{ members: Member[]; total: number; pages: number; current_page: number }>(
            "/api/members",
            { params },
        );
        return {
            items: response.data.members,
            total: response.data.total,
            pages: response.data.pages,
            current_page: response.data.current_page,
        };
    },

    getById: async (id: number) => {
        const response = await api.get<Member>(`/api/members/${id}`);
        return response.data;
    },

    create: async (data: Partial<Member>) => {
        const response = await api.post<Member>("/api/members", data);
        return response.data;
    },

    update: async (id: number, data: Partial<Member>) => {
        const response = await api.put<Member>(`/api/members/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        await api.delete(`/api/members/${id}`);
    },

    getClaims: async (id: number, params?: { page?: number; per_page?: number }) => {
        const response = await api.get(`/api/members/${id}/claims`, { params });
        return response.data;
    },
};
