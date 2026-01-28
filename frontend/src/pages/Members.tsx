import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useMembers } from "@/hooks/useMembers";
import { formatDate } from "@/lib/utils";
import type { Member } from "@/types";
import { ChevronLeft, ChevronRight, Plus, Search } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

export function Members() {
    const [page, setPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState("");
    const [search, setSearch] = useState("");

    const { data, isLoading } = useMembers({
        page,
        per_page: 20,
        search,
    });
    console.log("Members Data:", data);
    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        setSearch(searchQuery);
        setPage(1);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Members</h1>
                    <p className="text-muted-foreground">View and manage member information</p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Member
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>All Members</CardTitle>
                        <form onSubmit={handleSearch} className="flex items-center gap-2">
                            <Input
                                type="text"
                                placeholder="Search members..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-[300px]"
                            />
                            <Button type="submit" size="sm">
                                <Search className="h-4 w-4" />
                            </Button>
                        </form>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Member ID</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>DOB</TableHead>
                                <TableHead>Plan Type</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Email</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {isLoading ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center py-8">
                                        Loading...
                                    </TableCell>
                                </TableRow>
                            ) : data?.items.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} className="text-center py-8">
                                        No members found
                                    </TableCell>
                                </TableRow>
                            ) : (
                                data?.items.map((member: Member) => (
                                    <TableRow key={member.id}>
                                        <TableCell className="font-medium">
                                            <Link
                                                to={`/members/${member.id}`}
                                                className="text-sm font-medium transition-colors hover:text-primary"
                                            >
                                                {member.member_id}
                                            </Link>
                                        </TableCell>
                                        <TableCell>
                                            {member.first_name} {member.last_name}
                                        </TableCell>
                                        <TableCell>{formatDate(member.date_of_birth)}</TableCell>
                                        <TableCell>{member.plan_type}</TableCell>
                                        <TableCell>
                                            <Badge variant={member.is_active ? "success" : "warning"}>
                                                {member.is_active ? "Active" : "Inactive"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>{member.email}</TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>

                    <div className="flex items-center justify-between mt-4">
                        <div className="text-sm text-muted-foreground">
                            Showing {(page - 1) * 20 + 1} to {Math.min(page * 20, data?.total || 0)} of{" "}
                            {data?.total || 0} members
                        </div>
                        <div className="flex items-center gap-2">
                            <Button variant="outline" size="sm" onClick={() => setPage(page - 1)} disabled={page === 1}>
                                <ChevronLeft className="h-4 w-4" />
                                Previous
                            </Button>
                            <span className="text-sm">
                                Page {page} of {data?.pages || 1}
                            </span>
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setPage(page + 1)}
                                disabled={page === (data?.pages || 1)}
                            >
                                Next
                                <ChevronRight className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
