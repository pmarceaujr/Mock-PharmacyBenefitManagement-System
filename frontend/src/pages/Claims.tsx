import { ClaimsTable } from "@/components/claims/ClaimsTable";
import { Button } from "@/components/ui/button";
import { useClaims } from "@/hooks/useClaims";
import { Plus } from "lucide-react";
import { useState } from "react";

export function Claims() {
    const [page, setPage] = useState(1);
    const [status, setStatus] = useState<string>("");
    const [search, setSearch] = useState<string>("");

    const { data, isLoading } = useClaims({
        page,
        per_page: 20,
        status: status === "all" ? undefined : status,
    });
    console.log("Claims Data:", data);

    const handleStatusFilter = (newStatus: string) => {
        setStatus(newStatus);
        setPage(1); // Reset to first page when filtering
    };

    const handleSearch = (query: string) => {
        setSearch(query);
        setPage(1);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Claims</h1>
                    <p className="text-muted-foreground">Manage and review prescription claims</p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    New Claim
                </Button>
            </div>

            <ClaimsTable
                claims={data?.items || []}
                total={data?.total || 0}
                currentPage={page}
                totalPages={data?.pages || 1}
                onPageChange={setPage}
                onStatusFilter={handleStatusFilter}
                onSearch={handleSearch}
                isLoading={isLoading}
            />
        </div>
    );
}
