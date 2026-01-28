import { CostTrendChart } from "@/components/charts/CostTrendChart";
import { GenericVsBrandChart } from "@/components/charts/GenericVsBrandChart";
import { StatusBreakdownChart } from "@/components/charts/StatusBreakdownChart";
import { TopDrugsChart } from "@/components/charts/TopDrugsChart";
import { DashboardFilters } from "@/components/dashboard/DashboardFilters";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { useDashboard, useTrends } from "@/hooks/useAnalytics";
import { AlertCircle } from "lucide-react";
import { useState } from "react";

export function Dashboard() {
    const [selectedDays, setSelectedDays] = useState(30);

    const { data: dashboardData, isLoading: dashboardLoading, error: dashboardError } = useDashboard(selectedDays);
    const { data: trendsData, isLoading: trendsLoading } = useTrends(selectedDays);

    if (dashboardError) {
        return (
            <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>Failed to load dashboard data. Please try refreshing the page.</AlertDescription>
            </Alert>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-muted-foreground">Overview of prescription claims and analytics</p>
            </div>

            <DashboardFilters selectedDays={selectedDays} onDaysChange={setSelectedDays} />

            {dashboardLoading ? (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    {[...Array(4)].map((_, i) => (
                        <Skeleton key={i} className="h-[120px]" />
                    ))}
                </div>
            ) : dashboardData ? (
                <StatsCards
                    totalClaims={dashboardData.summary.total_claims}
                    totalCost={dashboardData.summary.total_cost}
                    averageCost={dashboardData.summary.average_cost}
                    periodDays={selectedDays}
                />
            ) : null}

            <div className="grid gap-6 md:grid-cols-2">
                {dashboardLoading ? (
                    <>
                        <Skeleton className="h-[400px]" />
                        <Skeleton className="h-[400px]" />
                    </>
                ) : dashboardData ? (
                    <>
                        <GenericVsBrandChart data={dashboardData.generic_vs_brand} />
                        <StatusBreakdownChart data={dashboardData.status_breakdown} />
                    </>
                ) : null}
            </div>

            {trendsLoading ? (
                <Skeleton className="h-[450px]" />
            ) : trendsData ? (
                <CostTrendChart
                    data={trendsData.trends}
                    title="Cost & Claims Trends"
                    description="Daily costs and claims with 7-day moving average"
                />
            ) : null}

            {dashboardLoading ? (
                <Skeleton className="h-[500px]" />
            ) : dashboardData ? (
                <TopDrugsChart data={dashboardData.top_drugs} />
            ) : null}
        </div>
    );
}
