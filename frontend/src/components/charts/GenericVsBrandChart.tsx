import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { Cell, Legend, Pie, PieChart, PieLabelRenderProps, ResponsiveContainer, Tooltip } from "recharts";

interface GenericVsBrandData {
    type: "Generic" | "Brand";
    claims: number;
    cost: number;
}

interface GenericVsBrandChartProps {
    data: GenericVsBrandData[];
}

const COLORS = {
    Generic: "#10b981",
    Brand: "#3b82f6",
};

// Define the label renderer
const pieLabel = (props: PieLabelRenderProps) => {
    // Safely access custom field from the original data entry
    // Recharts attaches the full data entry to props
    const { payload, percent } = props;

    // payload is the original data object → it has .type
    const type = (payload as GenericVsBrandData | undefined)?.type ?? "Unknown";

    if (percent === undefined) return null;

    return `${type}: ${(percent * 100).toFixed(0)}%`;
};
export function GenericVsBrandChart({ data }: GenericVsBrandChartProps) {
    const totalClaims = data.reduce((sum, item) => sum + item.claims, 0);
    const totalCost = data.reduce((sum, item) => sum + item.cost, 0);

    return (
        <Card>
            <CardHeader>
                <CardTitle>Generic vs Brand Distribution</CardTitle>
                <CardDescription>
                    {totalClaims.toLocaleString()} total claims | {formatCurrency(totalCost)} total cost
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <h4 className="text-sm font-medium mb-2">By Claims Count</h4>
                        <ResponsiveContainer width="100%" height={250}>
                            <PieChart>
                                <Pie
                                    data={data}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    // label={({ type, percent }) => `${type}: ${(percent * 100).toFixed(0)}%`}
                                    label={pieLabel}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="claims"
                                >
                                    {data.map((entry) => (
                                        <Cell key={entry.type} fill={COLORS[entry.type]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value: number | undefined) => {
                                        // Guard against undefined (rare in practice with valid data)
                                        if (value === undefined) return "N/A";

                                        return value.toLocaleString();
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div>
                        <h4 className="text-sm font-medium mb-2">By Total Cost</h4>
                        <ResponsiveContainer width="100%" height={250}>
                            <PieChart>
                                <Pie
                                    data={data}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={pieLabel}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="cost"
                                >
                                    {data.map((entry) => (
                                        <Cell key={entry.type} fill={COLORS[entry.type]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                                        border: "1px solid #ccc",
                                    }}
                                    formatter={(value: number | undefined, name: string | undefined) => {
                                        // Safe defaults if either is missing (rare, but satisfies TS)
                                        const safeName = name ?? "Unknown";
                                        const safeValue = value ?? 0;

                                        if (safeName.includes("cost")) {
                                            return formatCurrency(safeValue);
                                        }
                                        return safeValue.toFixed(0);
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
