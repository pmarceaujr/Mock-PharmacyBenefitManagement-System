import { Activity } from "lucide-react";
import { Link } from "react-router-dom";

export function Header() {
    return (
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center">
                <Link to="/" className="flex items-center space-x-2">
                    <Activity className="h-6 w-6 text-primary" />
                    <span className="text-xl font-bold">PrescriptionTracker - A Mock PBM</span>
                </Link>
                <nav className="ml-auto flex gap-6">
                    <Link to="/" className="text-sm font-medium transition-colors hover:text-primary">
                        Dashboard
                    </Link>
                    <Link to="/claims" className="text-sm font-medium transition-colors hover:text-primary">
                        Claims
                    </Link>
                    <Link to="/members" className="text-sm font-medium transition-colors hover:text-primary">
                        Members
                    </Link>
                    <Link to="/drugs" className="text-sm font-medium transition-colors hover:text-primary">
                        Drugs
                    </Link>
                    <Link to="/analytics" className="text-sm font-medium transition-colors hover:text-primary">
                        Analytics
                    </Link>
                </nav>
            </div>
        </header>
    );
}
