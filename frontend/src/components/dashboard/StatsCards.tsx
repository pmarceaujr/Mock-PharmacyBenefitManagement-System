import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { DollarSign, FileText, TrendingUp, Users } from "lucide-react";

interface StatsCardsProps {
    totalClaims: number;
    totalCost: number;
    averageCost: number;
    periodDays: number;
}

export function StatsCards({ totalClaims, totalCost, averageCost, periodDays }: StatsCardsProps) {
    const stats = [
        {
            title: "Total Claims",
            value: totalClaims.toLocaleString(),
            icon: FileText,
            description: `Last ${periodDays} days`,
        },
        {
            title: "Total Cost",
            value: formatCurrency(totalCost),
            icon: DollarSign,
            description: "All claims processed",
        },
        {
            title: "Average Cost",
            value: formatCurrency(averageCost),
            icon: TrendingUp,
            description: "Per claim",
        },
        {
            title: "Daily Average",
            value: (totalClaims / periodDays).toFixed(0),
            icon: Users,
            description: "Claims per day",
        },
    ];

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => {
                const Icon = stat.icon;
                return (
                    <Card key={stat.title}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                            <Icon className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stat.value}</div>
                            <p className="text-xs text-muted-foreground">{stat.description}</p>
                        </CardContent>
                    </Card>
                );
            })}
        </div>
    );
}
