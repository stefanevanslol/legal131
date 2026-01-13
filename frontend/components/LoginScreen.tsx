"use client";

import { useState, useEffect } from "react";
import { Lock, User, ArrowRight } from "lucide-react";

interface LoginScreenProps {
    onLogin: () => void;
}

export default function LoginScreen({ onLogin }: LoginScreenProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (username === "nick" && password === "86f3717d-d5f2-4be2-8af0-4280f87417bb") {
            localStorage.setItem("auth_token", "valid_session_token");
            onLogin(); // Notify parent that login is successful
        } else {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden">
                <div className="bg-blue-600 p-8 text-center">
                    <h1 className="text-3xl font-serif font-bold text-white mb-2">Conger Law AI</h1>
                    <p className="text-blue-100">Agentify AI Access Portal</p>
                </div>

                <div className="p-8">
                    <form onSubmit={handleLogin} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-2">Username</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <User size={18} className="text-slate-400" />
                                </div>
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors"
                                    placeholder="Enter username"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock size={18} className="text-slate-400" />
                                </div>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors"
                                    placeholder="Enter password"
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg flex items-center justify-center">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            className="w-full bg-slate-900 hover:bg-slate-800 text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-xl"
                        >
                            Access Dashboard <ArrowRight size={18} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
