import { memberService } from "@/services/memberService";
import type { Member } from "@/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useMembers(params?: { page?: number; per_page?: number; search?: string; is_active?: boolean }) {
    return useQuery({
        queryKey: ["members", params],
        queryFn: () => memberService.getAll(params),
    });
}

export function useMember(id: number) {
    return useQuery({
        queryKey: ["members", id],
        queryFn: () => memberService.getById(id),
        enabled: !!id,
    });
}

export function useCreateMember() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Member>) => memberService.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["members"] });
        },
    });
}

export function useUpdateMember() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Member> }) => memberService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["members"] });
        },
    });
}

export function useDeleteMember() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => memberService.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["members"] });
        },
    });
}
