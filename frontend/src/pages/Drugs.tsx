import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useDrugs } from "@/hooks/useDrugs";
import { formatDate } from "@/lib/utils";
import type { Drug } from "@/types";
import { ChevronLeft, ChevronRight, Plus, Search } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

export function Drugs() {
    const [page, setPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState("");
    const [search, setSearch] = useState("");

    const { data, isLoading } = useDrugs({
        page,
        per_page: 20,
        search,
    });
    console.log("Drugs Data:", data);
    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        setSearch(searchQuery);
        setPage(1);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Drugs</h1>
                    <p className="text-muted-foreground">View and manage drug information</p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Add Drug
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>All Drugs</CardTitle>
                        <form onSubmit={handleSearch} className="flex items-center gap-2">
                            <Input
                                type="text"
                                placeholder="Search drugs..."
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
                                {/* <TableHead>Drug ID</TableHead> */}
                                <TableHead>NDC</TableHead>
                                <TableHead>Drug Name</TableHead>
                                <TableHead>Generic</TableHead>
                                <TableHead>Therapeutic Class</TableHead>
                                <TableHead>Strength</TableHead>
                                <TableHead>Form</TableHead>
                                <TableHead>Route</TableHead>
                                <TableHead>Package Size</TableHead>
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
                                        No drugs found
                                    </TableCell>
                                </TableRow>
                            ) : (
                                data?.items.map((drug: Drug) => (
                                    <TableRow key={drug.id}>
                                        <TableCell className="font-medium">
                                            <Link
                                                to={`/drugs/${drug.id}`}
                                                className="text-sm font-medium transition-colors hover:text-primary"
                                            >
                                                {drug.ndc}
                                            </Link>
                                        </TableCell>
                                        {/* <TableCell>{drug.ndc}</TableCell> */}
                                        {/* <TableCell>{formatDate(drug.date_of_birth)}</TableCell> */}
                                        <TableCell>{drug.name || "N/A"}</TableCell>
                                        <TableCell>
                                            <Badge variant={drug.is_generic ? "success" : "warning"}>
                                                {drug.is_generic ? "Yes" : "No"}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>{drug.therapeutic_class}</TableCell>
                                        <TableCell>{drug.strength}</TableCell>
                                        <TableCell>{drug.dosage_form}</TableCell>
                                        <TableCell>{drug.route}</TableCell>
                                        <TableCell>{drug.package_size}</TableCell>
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
