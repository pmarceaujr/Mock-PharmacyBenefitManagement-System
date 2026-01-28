import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
import { useMember } from "@/hooks/useMembers";
import { Plus } from "lucide-react";
import { useParams } from "react-router-dom";

export function MemberDetail() {
    const { id } = useParams<{ id: string }>(); // Get ID from URL

    const memberId = id ? parseInt(id) : 0;

    const { data } = useMember(memberId);
    console.log("Member Data:", data);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Member Detail</h1>
                    <p className="text-muted-foreground">View and manage member information</p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Edit Member
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Detail Information for Member ID: {data?.id} </CardTitle>
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell className="font-medium">Member Id:</TableCell>
                                <TableCell> {data?.member_id} </TableCell>
                            </TableRow>

                            <TableRow>
                                <TableCell className="font-medium">Member Name</TableCell>
                                <TableCell>
                                    {data?.first_name} {data?.last_name}
                                </TableCell>
                            </TableRow>

                            <TableRow>
                                <TableCell className="font-medium">Address</TableCell>
                                <TableCell>
                                    {data?.address.line1}, {data?.address.city}, {data?.address.state},{" "}
                                    {data?.address.zip_code}
                                </TableCell>
                            </TableRow>

                            <TableRow>
                                <TableCell className="font-medium">Email</TableCell>
                                <TableCell>{data?.email}</TableCell>
                                <TableCell className="font-medium">Phone</TableCell>
                                <TableCell>{data?.phone}</TableCell>
                            </TableRow>

                            <TableRow>
                                <TableCell className="font-medium">DOB</TableCell>
                                <TableCell>{data?.date_of_birth}</TableCell>
                                <TableCell className="font-medium">Gender</TableCell>
                                <TableCell>{data?.gender}</TableCell>
                            </TableRow>

                            <TableRow>
                                <TableCell className="font-medium">Plan Type</TableCell>
                                <TableCell>{data?.plan_type}</TableCell>
                                <TableCell className="font-medium">Group Id</TableCell>
                                <TableCell>{data?.group_id}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell className="font-medium">Start Date</TableCell>
                                <TableCell>{data?.effective_date}</TableCell>
                                <TableCell className="font-medium">Status</TableCell>
                                <TableCell>
                                    <Badge variant={data?.is_active ? "success" : "warning"}>
                                        {data?.is_active ? "Active" : "Inactive"}
                                    </Badge>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
