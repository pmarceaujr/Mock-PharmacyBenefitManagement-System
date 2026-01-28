import { QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MainLayout } from "./components/layout/MainLayout";
import { queryClient } from "./lib/queryClient";
import { Analytics } from "./pages/Analytics";
import { Claims } from "./pages/Claims";
import { Dashboard } from "./pages/Dashboard";
import { DrugDetail } from "./pages/DrugDetail";
import { Drugs } from "./pages/Drugs";
import { MemberDetail } from "./pages/MemberDetail";
import { Members } from "./pages/Members";

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<MainLayout />}>
                        <Route index element={<Dashboard />} />
                        <Route path="claims" element={<Claims />} />
                        <Route path="members" element={<Members />} />
                        <Route path="members/:id" element={<MemberDetail />} />
                        <Route path="drugs" element={<Drugs />} />
                        <Route path="drugs/:id" element={<DrugDetail />} />
                        <Route path="analytics" element={<Analytics />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </QueryClientProvider>
    );
}
export default App;
