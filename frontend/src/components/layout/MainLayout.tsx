import { Outlet } from "react-router-dom";
import { Header } from "../ui/Header";

export function MainLayout() {
    return (
        <div className="min-h-screen bg-background">
            <Header />
            <main className="container m-[25px] py-6">
                <Outlet />
            </main>
        </div>
    );
}
