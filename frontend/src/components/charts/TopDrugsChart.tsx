import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface TopDrug {
    name: string;
    is_generic: boolean;
    claims: number;
    total_cost: number;
}

interface TopDrugsChartProps {
    data: TopDrug[];
    limit?: number;
}

export function TopDrugsChart({ data, limit = 10 }: TopDrugsChartProps) {
    const topDrugs = data.slice(0, limit);

    return (
        <Card>
            <CardHeader>
                <CardTitle>Top Drugs by Cost</CardTitle>
                <CardDescription>Highest cost medications in the period</CardDescription>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={topDrugs} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            type="number"
                            tick={{ fontSize: 12 }}
                            tickFormatter={(value) => `$${(value / 1000).toFixed(0)}K`}
                        />
                        <YAxis type="category" dataKey="name" tick={{ fontSize: 11 }} width={90} />
                        <Tooltip
                            contentStyle={{ backgroundColor: "rgba(255, 255, 255, 0.95)", border: "1px solid #ccc" }}
                            formatter={(value: number, name: string) => {
                                if (name === "total_cost") return formatCurrency(value);
                                return value;
                            }}
                            labelFormatter={(label: string) => `Drug: ${label}`}
                        />
                        <Legend />
                        <Bar dataKey="total_cost" fill="#3b82f6" name="Total Cost" radius={[0, 8, 8, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
