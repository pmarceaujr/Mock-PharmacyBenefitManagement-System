import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
import { useDrug } from "@/hooks/useDrugs";
// import { formatDate } from "@/lib/utils";
import { Plus } from "lucide-react";
import { useParams } from "react-router-dom";

export function DrugDetail() {
    const { id } = useParams<{ id: string }>(); // Get ID from URL

    const drugId = id ? parseInt(id) : 0;

    const { data } = useDrug(drugId);
    console.log("Drug Data:", data);

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
                        <CardTitle>Detail Information for Drug ID: {data?.ndc}</CardTitle>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell className="font-medium">NDC</TableCell>
                                <TableCell>{data?.ndc}</TableCell>
                                <TableCell className="font-medium">Active</TableCell>
                                <TableCell>
                                    <Badge variant={data?.is_active ? "success" : "warning"}>
                                        {data?.is_active ? "Yes" : "No"}
                                    </Badge>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell className="font-medium">Drug Name</TableCell>
                                <TableCell>{data?.name || "N/A"}</TableCell>
                                <TableCell className="font-medium">Generic Name</TableCell>
                                <TableCell>{data?.generic_name}</TableCell>
                                <TableCell className="font-medium">Generic</TableCell>
                                <TableCell>
                                    <Badge variant={data?.is_generic ? "success" : "warning"}>
                                        {data?.is_generic ? "Yes" : "No"}
                                    </Badge>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell className="font-medium">Therapeutic Class</TableCell>
                                <TableCell>{data?.therapeutic_class}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell className="font-medium">Strength</TableCell>
                                <TableCell>{data?.strength}</TableCell>
                                <TableCell className="font-medium">Form</TableCell>
                                <TableCell>{data?.dosage_form}</TableCell>
                                <TableCell className="font-medium">Route</TableCell>
                                <TableCell>{data?.route}</TableCell>
                                <TableCell className="font-medium">Package Size</TableCell>
                                <TableCell>{data?.package_size}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell className="font-medium">Manufacturer</TableCell>
                                <TableCell>{data?.manufacturer}</TableCell>
                                <TableCell className="font-medium">AWP</TableCell>
                                <TableCell>{data?.awp}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
