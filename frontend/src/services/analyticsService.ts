import type { CostSummaryReport, DashboardStats, GenericSavingsOpportunity, HighUtilizer, TrendData } from "@/types";
import { api } from "./api";

export const analyticsService = {
    getDashboard: async (days: number = 30) => {
        const response = await api.get<DashboardStats>("/api/analytics/dashboard", { params: { days } });
        return response.data;
    },

    getTrends: async (days: number = 90) => {
        const response = await api.get<TrendData>("/api/analytics/trends", { params: { days } });
        return response.data;
    },

    getHighUtilizers: async (days: number = 90, min_claims: number = 5) => {
        const response = await api.get<{ period_days: number; min_claims: number; high_utilizers: HighUtilizer[] }>(
            "/api/analytics/high-utilizers",
            { params: { days, min_claims } },
        );
        return response.data.high_utilizers;
    },

    getPharmacyPerformance: async (days: number = 90) => {
        const response = await api.get("/api/analytics/pharmacy-performance", {
            params: { days },
        });
        return response.data.pharmacies;
    },

    getTherapeuticClassBreakdown: async (days: number = 90) => {
        const response = await api.get("/api/analytics/therapeutic-class", {
            params: { days },
        });
        return response.data.therapeutic_classes;
    },

    getGenericSavings: async (days: number = 90) => {
        const response = await api.get<{
            period_days: number;
            total_potential_savings: number;
            opportunities: GenericSavingsOpportunity[];
        }>("/api/reports/generic-savings", { params: { days } });
        return response.data;
    },

    getCostSummary: async (start_date?: string, end_date?: string) => {
        const response = await api.get<CostSummaryReport>("/api/reports/cost-summary", {
            params: { start_date, end_date },
        });
        return response.data;
    },

    getMemberSummary: async (member_id: number, days: number = 365) => {
        const response = await api.get(`/api/reports/member-summary/${member_id}`, {
            params: { days },
        });
        return response.data;
    },
};
