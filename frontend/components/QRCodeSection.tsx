"use client";

import { useEffect, useState } from "react";
import { QRCodeSVG } from "qrcode.react";

interface QRCodeSectionProps {
  /** Override the chat URL embedded in the QR code */
  chatUrl?: string;
  className?: string;
}

export function QRCodeSection({ chatUrl, className }: QRCodeSectionProps) {
  const [url, setUrl] = useState<string>("");

  useEffect(() => {
    // Use the provided URL or derive from window.location
    if (chatUrl) {
      setUrl(chatUrl);
    } else {
      const origin = window.location.origin;
      setUrl(`${origin}/chat`);
    }
  }, [chatUrl]);

  if (!url) return null;

  return (
    <div className={`flex flex-col sm:flex-row items-center justify-center gap-8 ${className ?? ""}`}>
      {/* QR Code */}
      <div className="bg-white rounded-2xl p-5 shadow-chat-lg border border-gray-100 flex flex-col items-center gap-3">
        <QRCodeSVG
          value={url}
          size={180}
          bgColor="#ffffff"
          fgColor="#c2410c"
          level="H"
          includeMargin={false}
          imageSettings={{
            src: "",
            x: undefined,
            y: undefined,
            height: 0,
            width: 0,
            excavate: false,
          }}
        />
        <p className="text-xs text-gray-400 text-center font-medium">
          Scan to open AI Waiter chat
        </p>
      </div>

      {/* Instructions */}
      <div className="max-w-xs text-center sm:text-left">
        <h3 className="text-xl font-bold text-gray-900 mb-3">
          Table-ready in seconds 📱
        </h3>
        <ul className="space-y-2 text-gray-600 text-sm">
          {[
            "Print this QR code and place it on every table",
            "Customers scan with any smartphone camera",
            "Instant chat opens — no app download needed",
            "Works on all devices, always up-to-date",
          ].map((step) => (
            <li key={step} className="flex items-start gap-2">
              <span className="text-brand-500 font-bold mt-0.5">✓</span>
              {step}
            </li>
          ))}
        </ul>

        <div className="mt-4 p-3 bg-gray-50 rounded-xl border border-gray-100">
          <p className="text-xs text-gray-400 mb-1">Chat URL</p>
          <p className="text-xs font-mono text-gray-700 break-all">{url}</p>
        </div>
      </div>
    </div>
  );
}
