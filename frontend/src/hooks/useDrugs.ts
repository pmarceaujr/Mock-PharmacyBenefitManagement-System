import { drugService } from "@/services/drugService";
import type { Drug } from "@/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useDrugs(params?: { page?: number; per_page?: number; search?: string; is_active?: boolean }) {
    return useQuery({
        queryKey: ["drugs", params],
        queryFn: () => drugService.getAll(params),
    });
}

export function useDrug(id: number) {
    return useQuery({
        queryKey: ["drugs", id],
        queryFn: () => drugService.getById(id),
        enabled: !!id,
    });
}

export function useCreateDrug() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Drug>) => drugService.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["drugs"] });
        },
    });
}

export function useUpdateDrug() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Drug> }) => drugService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["drugs"] });
        },
    });
}

// export function useDeleteDrug() {
//     const queryClient = useQueryClient();

//     return useMutation({
//         mutationFn: (id: number) => drugService.delete(id),
//         onSuccess: () => {
//             queryClient.invalidateQueries({ queryKey: ["drugs"] });
//         },
//     });
// }
