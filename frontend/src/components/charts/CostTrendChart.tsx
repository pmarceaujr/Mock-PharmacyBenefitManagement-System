import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface TrendDataPoint {
    date: string;
    claims: number;
    cost: number;
    moving_avg_claims: number;
    moving_avg_cost: number;
}

interface CostTrendChartProps {
    data: TrendDataPoint[];
    title?: string;
    description?: string;
}

export function CostTrendChart({ data, title = "Cost Trends", description }: CostTrendChartProps) {
    const formattedData = data.map((item) => ({
        ...item,
        date: new Date(item.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    }));

    return (
        <Card>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
                {description && <CardDescription>{description}</CardDescription>}
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={formattedData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={80} />
                        <YAxis
                            yAxisId="left"
                            tick={{ fontSize: 12 }}
                            tickFormatter={(value) => `$${value.toLocaleString()}`}
                        />
                        <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ backgroundColor: "rgba(255, 255, 255, 0.95)", border: "1px solid #ccc" }}
                            formatter={(value: number, name: string) => {
                                if (name.includes("cost")) return formatCurrency(value);
                                return value.toFixed(0);
                            }}
                        />
                        <Legend />
                        <Line
                            yAxisId="left"
                            type="monotone"
                            dataKey="cost"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            name="Daily Cost"
                            dot={{ r: 3 }}
                        />
                        <Line
                            yAxisId="left"
                            type="monotone"
                            dataKey="moving_avg_cost"
                            stroke="#10b981"
                            strokeWidth={2}
                            strokeDasharray="5 5"
                            name="7-Day Avg Cost"
                            dot={false}
                        />
                        <Line
                            yAxisId="right"
                            type="monotone"
                            dataKey="claims"
                            stroke="#f59e0b"
                            strokeWidth={2}
                            name="Daily Claims"
                            dot={{ r: 3 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
