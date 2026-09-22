import { useEffect } from "react";
import { X } from "lucide-react";

export default function Modal({ open, onClose, title, subtitle, children }) {
  useEffect(() => {
    if (!open) return;
    function handleKey(e) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4 py-8">
      <div
        className="absolute inset-0 bg-ink/80 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="relative w-full max-w-lg rounded-xl border border-ink-line-strong bg-ink-panel shadow-panel">
        <div className="flex items-start justify-between border-b border-ink-line px-6 py-5">
          <div>
            <h2 className="font-serif text-xl text-parchment">{title}</h2>
            {subtitle && <p className="mt-1 text-[13.5px] text-parchment-dim">{subtitle}</p>}
          </div>
          <button
            onClick={onClose}
            className="rounded-md p-1 text-parchment-faint transition-colors hover:bg-ink-raised hover:text-parchment"
            aria-label="Close"
          >
            <X className="h-[18px] w-[18px]" />
          </button>
        </div>
        <div className="max-h-[70vh] overflow-y-auto px-6 py-5">{children}</div>
      </div>
    </div>
  );
}
