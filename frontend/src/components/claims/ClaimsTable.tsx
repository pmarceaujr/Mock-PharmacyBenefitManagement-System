import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatCurrency, formatDate } from "@/lib/utils";
import type { Claim } from "@/types";
import { ChevronLeft, ChevronRight, Search } from "lucide-react";
import { useState } from "react";

interface ClaimsTableProps {
    claims: Claim[];
    total: number;
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    onStatusFilter: (status: string) => void;
    onSearch: (query: string) => void;
    isLoading?: boolean;
}

const getStatusVariant = (status: string) => {
    switch (status) {
        case "paid":
            return "success";
        case "approved":
            return "default";
        case "pending":
            return "warning";
        case "denied":
            return "destructive";
        default:
            return "secondary";
    }
};

export function ClaimsTable({
    claims,
    total,
    currentPage,
    totalPages,
    onPageChange,
    onStatusFilter,
    onSearch,
    isLoading = false,
}: ClaimsTableProps) {
    const [searchQuery, setSearchQuery] = useState("");

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        onSearch(searchQuery);
    };

    return (
        <Card>
            <CardHeader>
                <div className="flex items-center justify-between">
                    <CardTitle>Claims</CardTitle>
                    <div className="flex items-center gap-4">
                        <form onSubmit={handleSearch} className="flex items-center gap-2">
                            <Input
                                type="text"
                                placeholder="Search claims..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-[250px]"
                            />
                            <Button type="submit" size="sm">
                                <Search className="h-4 w-4" />
                            </Button>
                        </form>
                        <Select onValueChange={onStatusFilter}>
                            <SelectTrigger className="w-[150px]">
                                <SelectValue placeholder="All statuses" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All statuses</SelectItem>
                                <SelectItem value="paid">Paid</SelectItem>
                                <SelectItem value="approved">Approved</SelectItem>
                                <SelectItem value="pending">Pending</SelectItem>
                                <SelectItem value="denied">Denied</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Claim #</TableHead>
                            <TableHead>Member</TableHead>
                            <TableHead>Drug</TableHead>
                            <TableHead>Generic</TableHead>
                            <TableHead>Fill Date</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="text-right">Total Cost</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow>
                                <TableCell colSpan={6} className="text-center py-8">
                                    Loading...
                                </TableCell>
                            </TableRow>
                        ) : claims.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={6} className="text-center py-8">
                                    No claims found
                                </TableCell>
                            </TableRow>
                        ) : (
                            claims.map((claim) => (
                                <TableRow key={claim.id}>
                                    <TableCell className="font-medium">{claim.claim_number}</TableCell>
                                    <TableCell>{claim.member_name || "N/A"}</TableCell>
                                    <TableCell>{claim.drug_name || "N/A"}</TableCell>
                                    <TableCell>
                                        <Badge variant={claim.is_generic ? "success" : "warning"}>
                                            {claim.is_generic ? "Yes" : "No"}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>{formatDate(claim.fill_date)}</TableCell>

                                    <TableCell>
                                        <Badge variant={getStatusVariant(claim.status)}>{claim.status}</Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        {formatCurrency(claim.pricing.total_cost)}
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>

                <div className="flex items-center justify-between mt-4">
                    <div className="text-sm text-muted-foreground">
                        Showing {(currentPage - 1) * 20 + 1} to {Math.min(currentPage * 20, total)} of {total} claims
                    </div>
                    <div className="flex items-center gap-2">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onPageChange(currentPage - 1)}
                            disabled={currentPage === 1}
                        >
                            <ChevronLeft className="h-4 w-4" />
                            Previous
                        </Button>
                        <span className="text-sm">
                            Page {currentPage} of {totalPages}
                        </span>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => onPageChange(currentPage + 1)}
                            disabled={currentPage === totalPages}
                        >
                            Next
                            <ChevronRight className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
