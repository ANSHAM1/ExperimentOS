const STATUS_STYLES = {
  connected: { dot: "bg-ok", text: "text-ok", label: "Connected" },
  error: { dot: "bg-flag", text: "text-flag", label: "Error" },
  testing: { dot: "bg-signal-bright animate-pulse", text: "text-signal-bright", label: "Testing…" },
  unverified: { dot: "bg-parchment-faint", text: "text-parchment-faint", label: "Unverified" },
};

export default function StatusDot({ status }) {
  const style = STATUS_STYLES[status] || STATUS_STYLES.unverified;
  return (
    <span className={`inline-flex items-center gap-1.5 text-[12.5px] ${style.text}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} />
      {style.label}
    </span>
  );
}
