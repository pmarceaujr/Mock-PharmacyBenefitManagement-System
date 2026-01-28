import { Outlet } from "react-router-dom";
import { Header } from "./Header";

export function MainLayout() {
    return (
        <div className="min-h-screen bg-background">
            <Header />
            <main className="container py-6">
                <Outlet />
            </main>
        </div>
    );
}
