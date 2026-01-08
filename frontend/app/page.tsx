import DashboardLayout from "@/components/DashboardLayout";
import Link from 'next/link';
import { FilePlus, Clock } from "lucide-react";

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




      </div>
    </DashboardLayout>
  );
}


