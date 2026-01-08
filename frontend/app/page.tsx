import DashboardLayout from "@/components/DashboardLayout";
import Link from 'next/link';
import { ArrowRight, FilePlus, Clock } from "lucide-react";

export default function Home() {
  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-900 to-slate-900 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden">
          <div className="relative z-10">
            <h1 className="text-3xl font-bold font-serif mb-2">Welcome back, Attorney Congero</h1>
            <p className="text-slate-300 max-w-lg">
              Ready to generate your next demand letter? Upload medical records to get started with our AI-powered extraction.
            </p>
            <Link href="/new-case" className="inline-flex items-center gap-2 mt-6 bg-blue-500 hover:bg-blue-400 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-lg shadow-blue-900/50">
              <FilePlus size={20} />
              Start New Case
            </Link>
          </div>
          {/* Abstract Background Decoration */}
          <div className="absolute right-0 top-0 h-full w-1/3 bg-white/5 skew-x-12 transform origin-bottom-right" />
        </div>

        {/* Recent Activity Grid */}
        <div>
          <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
            <Clock size={18} className="text-slate-400" />
            Recent Files
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Placeholder Cards */}

          </div>
        </div>

      </div>
    </DashboardLayout>
  );
}

function CaseCard({ client, date, status }: { client: string, date: string, status: string }) {
  const statusColor = {
    'Draft': 'bg-amber-100 text-amber-700',
    'Completed': 'bg-emerald-100 text-emerald-700',
    'Processing': 'bg-blue-100 text-blue-700'
  }[status] || 'bg-slate-100 text-slate-700';

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer group">
      <div className="flex justify-between items-start mb-4">
        <div className="h-10 w-10 bg-slate-50 text-slate-500 rounded-lg flex items-center justify-center font-bold text-lg group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
          {client.charAt(0)}
        </div>
        <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${statusColor}`}>
          {status}
        </span>
      </div>
      <h4 className="font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">{client}</h4>
      <p className="text-sm text-slate-500 mb-4">Last edited: {date}</p>
      <div className="flex items-center text-blue-600 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
        Open Case <ArrowRight size={16} className="ml-1" />
      </div>
    </div>
  )
}
