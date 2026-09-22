import { useId, useState } from "react";
import { Eye, EyeOff } from "lucide-react";

export default function Field({
  label,
  error,
  hint,
  type = "text",
  className = "",
  ...inputProps
}) {
  const id = useId();
  const [reveal, setReveal] = useState(false);
  const isPassword = type === "password";
  const resolvedType = isPassword && reveal ? "text" : type;

  return (
    <label htmlFor={id} className={`block ${className}`}>
      <span className="text-[13px] text-parchment-dim">{label}</span>
      <div className="relative mt-1.5">
        <input
          id={id}
          {...inputProps}
          type={resolvedType}
          className="w-full rounded-lg border border-ink-line bg-ink-raised px-3.5 py-2.5 text-[15px] text-parchment placeholder:text-parchment-faint transition-colors focus:border-signal-dim"
        />
        {isPassword && (
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setReveal((v) => !v)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-parchment-faint transition-colors hover:text-parchment-dim"
            aria-label={reveal ? "Hide password" : "Show password"}
          >
            {reveal ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        )}
      </div>
      {hint && !error && (
        <span className="mt-1.5 block text-[12.5px] text-parchment-faint">{hint}</span>
      )}
      {error && <span className="mt-1.5 block text-[13px] text-flag">{error}</span>}
    </label>
  );
}
