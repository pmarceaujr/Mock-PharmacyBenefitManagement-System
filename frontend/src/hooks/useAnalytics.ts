import { analyticsService } from "@/services/analyticsService";
import { useQuery } from "@tanstack/react-query";

export function useDashboard(days: number = 30) {
    return useQuery({
        queryKey: ["analytics", "dashboard", days],
        queryFn: () => analyticsService.getDashboard(days),
    });
}

export function useTrends(days: number = 90) {
    return useQuery({
        queryKey: ["analytics", "trends", days],
        queryFn: () => analyticsService.getTrends(days),
    });
}

export function useHighUtilizers(days: number = 90, min_claims: number = 5) {
    return useQuery({
        queryKey: ["analytics", "high-utilizers", days, min_claims],
        queryFn: () => analyticsService.getHighUtilizers(days, min_claims),
    });
}

export function useGenericSavings(days: number = 90) {
    return useQuery({
        queryKey: ["analytics", "generic-savings", days],
        queryFn: () => analyticsService.getGenericSavings(days),
    });
}

export function useCostSummary(start_date?: string, end_date?: string) {
    return useQuery({
        queryKey: ["analytics", "cost-summary", start_date, end_date],
        queryFn: () => analyticsService.getCostSummary(start_date, end_date),
    });
}
