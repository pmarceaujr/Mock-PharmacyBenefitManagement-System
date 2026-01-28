import { claimService } from "@/services/claimService";
import type { Claim } from "@/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useClaims(params?: {
    page?: number;
    per_page?: number;
    status?: string;
    member_id?: number;
    start_date?: string;
    end_date?: string;
}) {
    return useQuery({
        queryKey: ["claims", params],
        queryFn: () => claimService.getAll(params),
    });
}

export function useClaim(id: number) {
    return useQuery({
        queryKey: ["claims", id],
        queryFn: () => claimService.getById(id),
        enabled: !!id,
    });
}

export function useCreateClaim() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Claim>) => claimService.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["claims"] });
            queryClient.invalidateQueries({ queryKey: ["analytics"] });
        },
    });
}

export function useUpdateClaim() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Claim> }) => claimService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["claims"] });
            queryClient.invalidateQueries({ queryKey: ["analytics"] });
        },
    });
}
