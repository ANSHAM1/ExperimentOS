import { Database } from "lucide-react";

export default function DatabaseTypeCard({ type, onClick }) {
  return (
    <button
      onClick={onClick}
      className="group flex flex-col items-start gap-3 rounded-xl border border-ink-line bg-ink-panel px-4 py-4 text-left transition-all hover:-translate-y-0.5 hover:border-signal-dim hover:shadow-glow"
    >
      <span
        className="flex h-9 w-9 items-center justify-center rounded-lg border"
        style={{
          borderColor: `${type.accent}40`,
          backgroundColor: `${type.accent}14`,
          color: type.accent,
        }}
      >
        <Database className="h-[18px] w-[18px]" />
      </span>
      <span>
        <span className="block text-[14.5px] font-medium text-parchment">{type.label}</span>
        <span className="mt-0.5 block font-mono text-[11.5px] text-parchment-faint">
          {type.fileBased ? "file-based" : `default :${type.defaultPort}`}
        </span>
      </span>
    </button>
  );
}
