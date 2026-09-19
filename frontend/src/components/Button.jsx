export default function Button({ children, loading, ...props }) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className="flex w-full items-center justify-center gap-2 rounded-md bg-parchment px-4 py-2.5 text-[15px] font-medium text-ink transition-opacity hover:opacity-90 disabled:opacity-50"
    >
      {loading && (
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-ink/30 border-t-ink" />
      )}
      {children}
    </button>
  );
}
