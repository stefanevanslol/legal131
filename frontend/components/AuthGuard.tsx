"use client";

import { useEffect, useState } from "react";
import LoginScreen from "./LoginScreen";

export default function AuthGuard({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
        // Check for authentication on mount
        const token = localStorage.getItem("auth_token");
        if (token === "valid_session_token") {
            setIsAuthenticated(true);
        } else {
            setIsAuthenticated(false);
        }
    }, []);

    const handleLogin = () => {
        setIsAuthenticated(true);
    };

    if (isAuthenticated === null) {
        // Loading state, maybe show nothing or a spinner
        return null;
    }

    if (!isAuthenticated) {
        return <LoginScreen onLogin={handleLogin} />;
    }

    return <>{children}</>;
}
