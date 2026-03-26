"use client";

import Link from "next/link";
import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { QRCodeSection } from "@/components/QRCodeSection";
import { uploadMenu } from "@/lib/api";
import {
  MessageSquare,
  Zap,
  ShieldCheck,
  BarChart2,
  Upload,
  CheckCircle2,
  ChefHat,
  QrCode,
  ArrowRight,
  Loader2,
} from "lucide-react";

/* ── Feature cards data ──────────────────────────────────── */
const features = [
  {
    icon: <Zap className="w-6 h-6" />,
    title: "Instant Menu Q&A",
    desc: "Customers get accurate answers to menu questions in seconds — no waiting for a busy server.",
  },
  {
    icon: <ShieldCheck className="w-6 h-6" />,
    title: "Allergy & Diet Safe",
    desc: "The AI only answers from your uploaded menu data. No hallucinations. Always accurate.",
  },
  {
    icon: <MessageSquare className="w-6 h-6" />,
    title: "Natural Conversation",
    desc: "Multi-turn chat remembers context. Customers can ask follow-ups just like talking to a real waiter.",
  },
  {
    icon: <BarChart2 className="w-6 h-6" />,
    title: "Upsell Intelligence",
    desc: "The AI proactively suggests best sellers, add-ons, and pairings to increase average order value.",
  },
  {
    icon: <QrCode className="w-6 h-6" />,
    title: "QR Code Ready",
    desc: "Print or display a QR code on every table. Customers scan and start chatting immediately.",
  },
  {
    icon: <Upload className="w-6 h-6" />,
    title: "Excel Menu Upload",
    desc: "Just upload your menu as an Excel file and the AI is ready to serve — no coding required.",
  },
];

/* ── Main Page ────────────────────────────────────────────── */
export default function LandingPage() {
  const [uploadStatus, setUploadStatus] = useState<
    "idle" | "uploading" | "success" | "error"
  >("idle");
  const [uploadMsg, setUploadMsg] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleMenuUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus("uploading");
    setUploadMsg("");

    try {
      const result = await uploadMenu(file);
      setUploadStatus("success");
      setUploadMsg(result.message);
    } catch (err: unknown) {
      setUploadStatus("error");
      setUploadMsg(
        err instanceof Error ? err.message : "Upload failed. Please try again."
      );
    }
  }

  return (
    <main className="min-h-screen flex flex-col">
      {/* ── Navigation ── */}
      <nav className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ChefHat className="w-7 h-7 text-brand-500" />
            <span className="text-lg font-bold text-gray-900">AI Waiter</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/chat">
              <Button size="sm">Start Chat</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero Section ── */}
      <section className="hero-gradient pt-28 pb-24 px-4 text-white text-center">
        <div className="max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-white/15 backdrop-blur rounded-full px-4 py-1.5 text-sm font-medium mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-white" />
            </span>
            Powered by LangGraph Agentic RAG
          </div>

          <h1 className="text-5xl sm:text-6xl font-extrabold leading-tight mb-6">
            Meet your AI Waiter 👋
          </h1>
          <p className="text-xl sm:text-2xl text-orange-100 mb-10 leading-relaxed max-w-2xl mx-auto">
            Ready to answer questions, guide customers, and make service a
            breeze — 24 / 7, zero wait time.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/chat">
              <Button
                size="lg"
                className="bg-white text-brand-600 hover:bg-orange-50 shadow-lg w-full sm:w-auto gap-2"
              >
                Try the Chat Demo
                <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>

            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={uploadStatus === "uploading"}
              className="inline-flex items-center justify-center gap-2 h-12 px-8 rounded-lg border-2 border-white/60 text-white font-semibold hover:bg-white/10 transition-colors disabled:opacity-60"
            >
              {uploadStatus === "uploading" ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Uploading…
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Upload Menu
                </>
              )}
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".xlsx,.xls"
              className="hidden"
              onChange={handleMenuUpload}
            />
          </div>

          {/* Upload feedback */}
          {uploadMsg && (
            <div
              className={`mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium ${
                uploadStatus === "success"
                  ? "bg-green-500/20 text-green-100"
                  : "bg-red-500/20 text-red-100"
              }`}
            >
              {uploadStatus === "success" ? (
                <CheckCircle2 className="w-4 h-4" />
              ) : null}
              {uploadMsg}
            </div>
          )}
        </div>
      </section>

      {/* ── Stats Strip ── */}
      <section className="bg-brand-700 text-white py-8 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-3 gap-6 text-center">
          {[
            { value: "< 2s", label: "Response time" },
            { value: "100%", label: "Menu accuracy" },
            { value: "24 / 7", label: "Always available" },
          ].map(({ value, label }) => (
            <div key={label}>
              <div className="text-3xl font-extrabold text-brand-200">{value}</div>
              <div className="text-sm text-brand-300 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-4">
              Everything a great waiter does — automated
            </h2>
            <p className="text-gray-500 text-lg max-w-xl mx-auto">
              Upload your menu once. The AI handles the rest.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div
                key={f.title}
                className="bg-white rounded-2xl p-6 shadow-chat hover:shadow-chat-lg transition-shadow"
              >
                <div className="w-11 h-11 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center mb-4">
                  {f.icon}
                </div>
                <h3 className="font-bold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-extrabold text-gray-900 text-center mb-14">
            Up and running in 3 steps
          </h2>
          <div className="relative">
            {/* connector line */}
            <div className="hidden sm:block absolute left-6 top-8 bottom-8 w-0.5 bg-brand-100" />
            <div className="space-y-8">
              {[
                {
                  step: "1",
                  title: "Upload your menu",
                  desc: "Export your menu as Excel and upload it. AI Waiter parses every dish, price, and allergen automatically.",
                },
                {
                  step: "2",
                  title: "Share the QR code",
                  desc: "Print the generated QR code or paste the link. Customers scan it and start chatting instantly.",
                },
                {
                  step: "3",
                  title: "Watch customers get served",
                  desc: "The AI answers questions, suggests dishes, and upsells — while your staff focuses on delivering great food.",
                },
              ].map(({ step, title, desc }) => (
                <div key={step} className="flex gap-6">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-brand-500 text-white font-bold text-lg flex items-center justify-center shadow z-10">
                    {step}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg mb-1">
                      {title}
                    </h3>
                    <p className="text-gray-500 leading-relaxed">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── QR Code Section ── */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-extrabold text-gray-900 mb-3">
              Scan to start chatting 📱
            </h2>
            <p className="text-gray-500">
              Point your phone camera at this QR code to open the AI Waiter chat.
            </p>
          </div>
          <QRCodeSection />
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="hero-gradient py-20 px-4 text-white text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl font-extrabold mb-6">
            Your AI Waiter is ready to serve 👋
          </h2>
          <p className="text-orange-100 text-lg mb-10">
            Join restaurants transforming customer experience with intelligent AI.
          </p>
          <Link href="/chat">
            <Button
              size="lg"
              className="bg-white text-brand-600 hover:bg-orange-50 gap-2"
            >
              Start Chatting Now
              <ArrowRight className="w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4 text-center text-sm">
        <div className="flex items-center justify-center gap-2 mb-3">
          <ChefHat className="w-5 h-5 text-brand-400" />
          <span className="text-white font-semibold">AI Waiter</span>
        </div>
        <p>
          Built with Next.js · FastAPI · LangGraph · Supabase pgvector
        </p>
      </footer>
    </main>
  );
}
