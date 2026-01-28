import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Cell, Legend, Pie, PieChart, PieLabelRenderProps, ResponsiveContainer, Tooltip } from "recharts";

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

// Define the label renderer
const pieLabel = (props: PieLabelRenderProps) => {
    // Safely access custom field from the original data entry
    // Recharts attaches the full data entry to props
    const { payload, percent } = props;

    // payload is the original data object → it has .type
    const type = (payload as StatusData | undefined)?.status ?? "Unknown";

    if (percent === undefined) return null;

    return `${type}: ${(percent * 100).toFixed(0)}%`;
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
                            label={pieLabel}
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="count"
                        >
                            {data.map((entry) => (
                                <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || "#8884d8"} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{ backgroundColor: "rgba(255, 255, 255, 0.95)", border: "1px solid #ccc" }}
                            formatter={(
                                value: number | undefined, // Recharts allows undefined
                                _name: string | undefined, // name is unused here, but must accept | undefined
                            ) => {
                                // In a well-formed chart this will never be undefined, but we satisfy TS
                                if (value === undefined || value === null) return "0 (0.0%)";

                                const percentage = totalClaims ? (value / totalClaims) * 100 : 0;

                                return `${value.toLocaleString()} (${percentage.toFixed(1)}%)`;
                            }}
                        />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
