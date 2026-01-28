import { DashboardFilters } from "@/components/dashboard/DashboardFilters";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useGenericSavings, useHighUtilizers } from "@/hooks/useAnalytics";
import { formatCurrency } from "@/lib/utils";
import { TrendingDown, Users } from "lucide-react";
import { useState } from "react";

export function Analytics() {
    const [selectedDays, setSelectedDays] = useState(90);

    const { data: savingsData, isLoading: savingsLoading } = useGenericSavings(selectedDays);
    const { data: utilizersData, isLoading: utilizersLoading } = useHighUtilizers(selectedDays);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
                <p className="text-muted-foreground">Advanced analytics and cost optimization insights</p>
            </div>

            <DashboardFilters selectedDays={selectedDays} onDaysChange={setSelectedDays} />

            <Tabs defaultValue="savings" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="savings">
                        <TrendingDown className="mr-2 h-4 w-4" />
                        Savings Opportunities
                    </TabsTrigger>
                    <TabsTrigger value="utilizers">
                        <Users className="mr-2 h-4 w-4" />
                        High Utilizers
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="savings" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-3">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Total Potential Savings</CardTitle>
                                <TrendingDown className="h-4 w-4 text-green-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-green-600">
                                    {savingsLoading ? "..." : formatCurrency(savingsData?.total_potential_savings || 0)}
                                </div>
                                <p className="text-xs text-muted-foreground">From generic substitutions</p>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Opportunities</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">
                                    {savingsLoading ? "..." : savingsData?.opportunities.length || 0}
                                </div>
                                <p className="text-xs text-muted-foreground">Identified drugs</p>
                            </CardContent>
                        </Card>
                    </div>

                    <Card>
                        <CardHeader>
                            <CardTitle>Generic Substitution Opportunities</CardTitle>
                            <CardDescription>Brand drugs with available generic alternatives</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Brand Drug</TableHead>
                                        <TableHead>Generic Alternative</TableHead>
                                        <TableHead className="text-right">Claims</TableHead>
                                        <TableHead className="text-right">Avg Brand Cost</TableHead>
                                        <TableHead className="text-right">Avg Generic Cost</TableHead>
                                        <TableHead className="text-right">Potential Savings</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {savingsLoading ? (
                                        <TableRow>
                                            <TableCell colSpan={6} className="text-center py-8">
                                                Loading...
                                            </TableCell>
                                        </TableRow>
                                    ) : savingsData?.opportunities.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={6} className="text-center py-8">
                                                No opportunities found
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        savingsData?.opportunities.map((opp, index) => (
                                            <TableRow key={index}>
                                                <TableCell className="font-medium">{opp.brand_name}</TableCell>
                                                <TableCell>{opp.generic_name}</TableCell>
                                                <TableCell className="text-right">{opp.brand_claims}</TableCell>
                                                <TableCell className="text-right">
                                                    {formatCurrency(opp.avg_brand_cost)}
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    {formatCurrency(opp.avg_generic_cost)}
                                                </TableCell>
                                                <TableCell className="text-right font-bold text-green-600">
                                                    {formatCurrency(opp.potential_savings)}
                                                </TableCell>
                                            </TableRow>
                                        ))
                                    )}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="utilizers" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>High Utilizers</CardTitle>
                            <CardDescription>Members with highest claim volume and costs</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Member ID</TableHead>
                                        <TableHead>Name</TableHead>
                                        <TableHead className="text-right">Claims</TableHead>
                                        <TableHead className="text-right">Total Cost</TableHead>
                                        <TableHead className="text-right">Avg Per Claim</TableHead>
                                        <TableHead>Risk Level</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {utilizersLoading ? (
                                        <TableRow>
                                            <TableCell colSpan={6} className="text-center py-8">
                                                Loading...
                                            </TableCell>
                                        </TableRow>
                                    ) : utilizersData?.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={6} className="text-center py-8">
                                                No high utilizers found
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        utilizersData?.map((utilizer, index) => {
                                            const riskLevel =
                                                utilizer.total_cost > 5000
                                                    ? "high"
                                                    : utilizer.total_cost > 2000
                                                      ? "medium"
                                                      : "low";
                                            return (
                                                <TableRow key={index}>
                                                    <TableCell className="font-medium">{utilizer.member_id}</TableCell>
                                                    <TableCell>{utilizer.name}</TableCell>
                                                    <TableCell className="text-right">{utilizer.claim_count}</TableCell>
                                                    <TableCell className="text-right">
                                                        {formatCurrency(utilizer.total_cost)}
                                                    </TableCell>
                                                    <TableCell className="text-right">
                                                        {formatCurrency(utilizer.avg_cost_per_claim)}
                                                    </TableCell>
                                                    <TableCell>
                                                        <Badge
                                                            variant={
                                                                riskLevel === "high"
                                                                    ? "destructive"
                                                                    : riskLevel === "medium"
                                                                      ? "warning"
                                                                      : "secondary"
                                                            }
                                                        >
                                                            {riskLevel.toUpperCase()}
                                                        </Badge>
                                                    </TableCell>
                                                </TableRow>
                                            );
                                        })
                                    )}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
