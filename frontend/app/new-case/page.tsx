"use client"
import { useState } from 'react';
import DashboardLayout from "@/components/DashboardLayout";
import { UploadCloud, FileText, CheckCircle2, Loader2, Play, X } from "lucide-react";
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

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            const newFiles = Array.from(e.target.files);
            // Append new files to existing ones, avoiding duplicates based on name and size if desired, 
            // but for now simple append is fine or we can filter. 
            // Let's allow duplicates as different versions might be intended, or just simple append.
            setFiles(prev => [...prev, ...newFiles]);

            // Reset input so same file can be selected again if needed
            e.target.value = "";
        }
    };

    const removeFile = (index: number) => {
        setFiles(prev => prev.filter((_, i) => i !== index));
    };

    const handleAnalyze = async () => {
        if (files.length === 0) return;

        setIsUploading(true);
        const formData = new FormData();
        files.forEach(file => {
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
            throw err; // Re-throw to be caught by handleAnalyze
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
                            {isUploading ? (
                                // Analyzing View
                                <div className="flex flex-col items-center animate-in fade-in zoom-in duration-300">
                                    <div className="w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center mb-6 text-blue-500 animate-pulse">
                                        <Loader2 size={40} className="animate-spin" />
                                    </div>
                                    <h3 className="text-xl font-medium text-slate-800 mb-2">Analyzing Documents...</h3>
                                    <p className="text-slate-500 text-center max-w-md">
                                        Processing {files.length} file(s). This may take a moment.
                                    </p>
                                </div>
                            ) : (
                                // Upload View
                                <>
                                    <div className="w-20 h-20 rounded-full bg-blue-50 flex items-center justify-center mb-6 text-blue-500 transition-transform hover:scale-105 duration-300">
                                        <UploadCloud size={32} />
                                    </div>

                                    <h3 className="text-xl font-medium text-slate-800 mb-2">Upload Medical Records</h3>
                                    <p className="text-slate-500 text-center max-w-md mb-8">
                                        Drag & drop PDFs here or browse to upload.
                                        <br />
                                        Add files one by one or in batches.
                                    </p>

                                    {/* File List */}
                                    {files.length > 0 && (
                                        <div className="w-full max-w-md mb-8 space-y-3">
                                            {files.map((file, idx) => (
                                                <div key={idx} className="flex items-center justify-between bg-slate-50 p-3 rounded-lg border border-slate-100 group hover:border-blue-200 transition-colors">
                                                    <div className="flex items-center gap-3 overflow-hidden">
                                                        <div className="p-2 bg-white rounded-md text-slate-400">
                                                            <FileText size={18} />
                                                        </div>
                                                        <div className="flex flex-col min-w-0">
                                                            <span className="text-sm font-medium text-slate-700 truncate">{file.name}</span>
                                                            <span className="text-xs text-slate-400">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                                                        </div>
                                                    </div>
                                                    <button
                                                        onClick={() => removeFile(idx)}
                                                        className="text-slate-400 hover:text-red-500 p-2 hover:bg-red-50 rounded-full transition-colors"
                                                        title="Remove file"
                                                    >
                                                        <X size={18} />
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    <div className="flex gap-4">
                                        <label className="relative cursor-pointer">
                                            <span className={cn(
                                                "px-6 py-2.5 rounded-lg font-medium transition-all duration-200 border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 shadow-sm",
                                                files.length === 0 ? "bg-blue-600 text-white border-transparent hover:bg-blue-700 hover:border-transparent shadow-md hover:shadow-lg" : ""
                                            )}>
                                                {files.length === 0 ? "Browse Files" : "Add More Files"}
                                            </span>
                                            <input type="file" accept=".pdf" multiple className="hidden" onChange={handleFileUpload} />
                                        </label>

                                        {files.length > 0 && (
                                            <button
                                                onClick={handleAnalyze}
                                                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2.5 rounded-lg font-medium transition-all shadow-md hover:shadow-lg flex items-center gap-2 animate-in fade-in slide-in-from-bottom-2"
                                            >
                                                <Play size={16} fill="currentColor" />
                                                Analyze {files.length} File{files.length !== 1 ? 's' : ''}
                                            </button>
                                        )}
                                    </div>
                                </>
                            )}
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
