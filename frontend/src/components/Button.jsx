const VARIANTS = {
  primary:
    "bg-signal text-ink hover:bg-signal-bright disabled:hover:bg-signal shadow-[0_1px_0_rgba(255,255,255,0.18)_inset]",
  secondary:
    "bg-ink-raised text-parchment border border-ink-line-strong hover:border-signal-dim hover:text-parchment",
  ghost:
    "bg-transparent text-parchment-dim hover:text-parchment hover:bg-ink-raised",
  danger:
    "bg-transparent text-flag border border-flag/30 hover:bg-flag/10",
};

export default function Button({
  children,
  loading,
  variant = "primary",
  className = "",
  ...props
}) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[14.5px] font-medium transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-50 ${VARIANTS[variant]} ${className}`}
    >
      {loading && (
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-current/30 border-t-current" />
      )}
      {children}
    </button>
  );
}
