import { createContext, useCallback, useContext, useRef, useState } from "react";
import { CheckCircle2, XCircle, X } from "lucide-react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const idRef = useRef(0);

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const push = useCallback(
    (message, variant = "ok") => {
      const id = ++idRef.current;
      setToasts((prev) => [...prev, { id, message, variant }]);
      setTimeout(() => dismiss(id), 4200);
    },
    [dismiss],
  );

  const toast = {
    success: (message) => push(message, "ok"),
    error: (message) => push(message, "error"),
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="pointer-events-none fixed inset-x-0 top-0 z-[100] flex flex-col items-center gap-2 px-4 py-4 sm:items-end sm:px-6">
        {toasts.map((t) => (
          <div
            key={t.id}
            role="status"
            className="pointer-events-auto flex w-full max-w-sm items-start gap-2.5 rounded-lg border border-ink-line bg-ink-raised/95 px-4 py-3 shadow-panel backdrop-blur"
          >
            {t.variant === "ok" ? (
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-ok" />
            ) : (
              <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-flag" />
            )}
            <p className="flex-1 text-[13.5px] leading-snug text-parchment">{t.message}</p>
            <button
              onClick={() => dismiss(t.id)}
              className="mt-0.5 text-parchment-faint transition-colors hover:text-parchment"
              aria-label="Dismiss"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within a ToastProvider");
  return ctx;
}
