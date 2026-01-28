import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface DashboardFiltersProps {
    selectedDays: number;
    onDaysChange: (days: number) => void;
}

export function DashboardFilters({ selectedDays, onDaysChange }: DashboardFiltersProps) {
    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                    <Label htmlFor="days-filter" className="whitespace-nowrap">
                        Time Period:
                    </Label>
                    <Select value={selectedDays.toString()} onValueChange={(value) => onDaysChange(Number(value))}>
                        <SelectTrigger id="days-filter" className="w-[180px]">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="7">Last 7 days</SelectItem>
                            <SelectItem value="30">Last 30 days</SelectItem>
                            <SelectItem value="60">Last 60 days</SelectItem>
                            <SelectItem value="90">Last 90 days</SelectItem>
                            <SelectItem value="180">Last 6 months</SelectItem>
                            <SelectItem value="365">Last year</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </CardContent>
        </Card>
    );
}
