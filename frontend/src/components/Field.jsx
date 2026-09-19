export default function Field({ label, error, ...inputProps }) {
  return (
    <label className="block">
      <span className="text-[13px] text-parchment-dim">{label}</span>
      <input
        {...inputProps}
        className="mt-1.5 w-full rounded-md border border-ink-line bg-ink-panel px-3.5 py-2.5 text-[15px] text-parchment placeholder:text-parchment-dim/60 transition-colors focus:border-signal-dim"
      />
      {error && <span className="mt-1.5 block text-[13px] text-flag">{error}</span>}
    </label>
  );
}
