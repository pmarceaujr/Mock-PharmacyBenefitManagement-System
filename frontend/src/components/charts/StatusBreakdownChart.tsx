import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

interface StatusData {
    status: string;
    count: number;
}

interface StatusBreakdownChartProps {
    data: StatusData[];
}

const STATUS_COLORS: Record<string, string> = {
    paid: "#10b981",
    approved: "#3b82f6",
    pending: "#f59e0b",
    denied: "#ef4444",
    reversed: "#6b7280",
};

export function StatusBreakdownChart({ data }: StatusBreakdownChartProps) {
    const totalClaims = data.reduce((sum, item) => sum + item.count, 0);

    return (
        <Card>
            <CardHeader>
                <CardTitle>Claims by Status</CardTitle>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ status, percent }) => `${status}: ${(percent * 100).toFixed(0)}%`}
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="count"
                        >
                            {data.map((entry) => (
                                <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || "#8884d8"} />
                            ))}
                        </Pie>
                        <Tooltip
                            formatter={(value: number) =>
                                `${value.toLocaleString()} (${((value / totalClaims) * 100).toFixed(1)}%)`
                            }
                        />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
