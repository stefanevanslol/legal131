"use client"
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, CloudUpload, FileText, Settings, LogOut } from 'lucide-react';
import { cn } from '@/lib/utils'; // Assuming you have a utils file for clsx/tailwind-merge

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="flex h-screen bg-slate-50 text-slate-900 font-sans">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 text-white flex flex-col shadow-xl">
                <div className="p-6 border-b border-slate-800">
                    <h1 className="text-2xl font-serif font-bold tracking-wide text-blue-400">
                        Agentify<span className="text-white">AI</span>
                    </h1>
                    <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Congero Law Automation</p>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <NavItem href="/" icon={<LayoutDashboard size={20} />} label="Overview" />
                    <NavItem href="/new-case" icon={<CloudUpload size={20} />} label="New Case" />

                </nav>


            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm">
                    <h2 className="text-lg font-medium text-slate-700">Dashboard</h2>
                    <div className="flex items-center gap-4">
                        <div className="h-8 w-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
                            NG
                        </div>
                    </div>
                </header>
                <div className="p-8 max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    )
}

function NavItem({ href, icon, label }: { href: string; icon: React.ReactNode; label: string }) {
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <Link
            href={href}
            className={cn(
                "flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200",
                isActive
                    ? "bg-blue-600 text-white shadow-md shadow-blue-900/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800"
            )}
        >
            {icon}
            <span>{label}</span>
        </Link>
    )
}
