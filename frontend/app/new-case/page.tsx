"use client"
import { useState } from 'react';
import DashboardLayout from "@/components/DashboardLayout";
import { CloudUpload, FileText, CheckCircle2, Loader2, Play, X } from "lucide-react";
import { cn } from '@/lib/utils';
import Image from 'next/image';

type AnalysisResult = {
    // Basic Info
    yourInsuredName: string;
    "ClaimNo ": string; // Note space
    DateOfLoss: string;
    clientName: string;
    refferToClient: string;

    // Medical Info
    medicalFacility: string;
    TreatingPhysician: string;
    TypeTreatment: string;
    DatesOfTreaments: string;

    // Diagnosis & Treatment
    complaintsByclient: string;
    TreatmentsAndDiagnosses: string;
    TreatmentsAndDiagnosses2: string;

    // Narrative
    clientDescription: string;
    clientLastName: string;
    clientsProblems: string;

    // Finances
    medicalTreamentCostAndPsysican: string;
    totalBilled: string;
    totalOutStand: string;

    // Other
    surgicalRecommendations: string;
    ListOfMedicalRecords: string;
} | null;

export default function NewCasePage() {
    const [step, setStep] = useState<1 | 2 | 3>(1);
    const [isUploading, setIsUploading] = useState(false);
    const [files, setFiles] = useState<File[]>([]);
    const [data, setData] = useState<AnalysisResult>(null);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            console.log("File selected:", e.target.files.length);
            const selectedFiles = Array.from(e.target.files);
            setFiles(selectedFiles);
            setIsUploading(true);

            // Reset input
            e.target.value = "";

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });

            try {
                // 1. Analyze
                // Direct file upload to backend to avoid Next.js proxy timeout
                const res = await fetch('http://localhost:8000/api/analyze', {
                    method: 'POST',
                    body: formData,
                });

                if (!res.ok) {
                    const errorText = await res.text();
                    throw new Error(`Analysis failed: ${errorText}`);
                }

                const result = await res.json();
                const extracted = result.extracted_data;
                setData(extracted);

                // 2. Auto-Generate Document
                await generateDocument(extracted);

            } catch (err) {
                console.error(err);
                alert(err instanceof Error ? err.message : "Failed to analyze/generate");
            } finally {
                setIsUploading(false);
            }
        }
    };

    const generateDocument = async (dataToUse: AnalysisResult) => {
        if (!dataToUse) return;
        try {
            const res = await fetch('http://localhost:8000/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: dataToUse }),
            });

            if (!res.ok) throw new Error("Generation failed");

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Demand_Letter_${dataToUse.clientName || 'Draft'}.docx`;
            document.body.appendChild(a);
            a.click();
            a.remove();

        } catch (err) {
            console.error(err);
            throw err; // Re-throw to be caught by handleFileUpload
        }
    }

    return (
        <DashboardLayout>
            <div className="max-w-4xl mx-auto">
                <h1 className="text-2xl font-serif font-bold text-slate-900 mb-6">Create New Demand Letter</h1>

                {/* Stepper */}
                <div className="flex items-center justify-between mb-12 relative">
                    <div className="absolute top-1/2 left-0 w-full h-1 bg-slate-200 -z-10 transform -translate-y-1/2 rounded-full" />
                    <StepIndicator number={1} label="Upload Records" active={step >= 1} current={step === 1} />
                    <StepIndicator number={2} label="Review Analysis" active={step >= 2} current={step === 2} />
                    <StepIndicator number={3} label="Download Demand" active={step >= 3} current={step === 3} />
                </div>

                {/* content */}
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 min-h-[400px]">
                    {step === 1 && (
                        <div className="flex flex-col items-center justify-center h-full py-12">
                            <div className={cn("w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center mb-6 text-blue-500", isUploading && "animate-pulse")}>
                                {isUploading ? <Loader2 size={40} className="animate-spin" /> : <UploadCloud size={40} />}
                            </div>

                            <h3 className="text-xl font-medium text-slate-800 mb-2">
                                {isUploading ? "Analyzing Document..." : "Upload Medical Records"}
                            </h3>
                            <p className="text-slate-500 text-center max-w-md mb-8">
                                {isUploading
                                    ? `Analyzing ${files.length} Document(s)...`
                                    : "Drag & drop your PDFs here or browse to upload. We support multiple files."}
                            </p>

                            <label className={cn("relative cursor-pointer", isUploading && "pointer-events-none opacity-50")}>
                                <span className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors shadow-lg shadow-blue-900/20">
                                    Browse Files
                                </span>
                                <input type="file" accept=".pdf" multiple className="hidden" onChange={handleFileUpload} />
                            </label>
                        </div>
                    )}

                    {/* Step 2 Review removed for auto-generation */}

                    {step === 3 && (
                        <div className="flex flex-col items-center justify-center py-12 text-center">
                            <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mb-6">
                                <CheckCircle2 size={40} />
                            </div>
                            <h3 className="text-2xl font-bold text-slate-900 mb-2">Demand Letter Ready!</h3>
                            <p className="text-slate-500 mb-8 max-w-sm">
                                Your document has been generated and downloaded. You can find it in your downloads folder.
                            </p>
                            <button
                                className="bg-slate-900 text-white px-8 py-3 rounded-lg font-medium hover:bg-slate-800 transition-colors"
                                onClick={() => { setStep(1); setData(null); }}
                            >
                                Create Another
                            </button>
                        </div>
                    )}
                </div>

            </div>
        </DashboardLayout>
    )
}

function StepIndicator({ number, label, active, current }: { number: number, label: string, active: boolean, current: boolean }) {
    return (
        <div className={cn("flex flex-col items-center gap-2 z-10 transition-all duration-300", current ? "scale-105" : "opacity-70")}>
            <div className={cn(
                "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm border-4 transition-colors duration-300",
                active ? "bg-blue-600 border-blue-100 text-white" : "bg-white border-slate-200 text-slate-400"
            )}>
                {active ? <CheckCircle2 size={20} /> : number}
            </div>
            <span className={cn(
                "text-sm font-medium",
                active ? "text-blue-900" : "text-slate-400"
            )}>{label}</span>
        </div>
    )
}
