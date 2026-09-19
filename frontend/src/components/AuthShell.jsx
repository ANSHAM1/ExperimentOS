export default function AuthShell({ eyebrow, title, subtitle, children }) {
  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[1fr_1fr]">
      <div className="flex items-center justify-center px-6 py-16 sm:px-10">
        <div className="w-full max-w-sm">
          <a href="/" className="font-serif text-[22px] tracking-tight text-parchment">
            Signal
          </a>
          <div className="mt-10">
            <p className="text-sm text-signal-bright">{eyebrow}</p>
            <h1 className="mt-2 font-serif text-3xl leading-tight text-parchment">{title}</h1>
            {subtitle && <p className="mt-3 text-[15px] leading-relaxed text-parchment-dim">{subtitle}</p>}
          </div>
          <div className="mt-8">{children}</div>
        </div>
      </div>

      <ConsolePreview />
    </div>
  );
}

function ConsolePreview() {
  return (
    <div className="relative hidden overflow-hidden border-l border-ink-line bg-ink-panel lg:flex lg:items-center lg:justify-center">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage:
            "linear-gradient(to right, #ECE8DF 1px, transparent 1px), linear-gradient(to bottom, #ECE8DF 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />
      <div className="relative w-full max-w-md rounded-lg border border-ink-line bg-ink shadow-panel">
        <div className="flex items-center gap-2 border-b border-ink-line px-4 py-3">
          <span className="h-2.5 w-2.5 rounded-full bg-parchment-dim/40" />
          <span className="h-2.5 w-2.5 rounded-full bg-parchment-dim/40" />
          <span className="h-2.5 w-2.5 rounded-full bg-signal" />
          <span className="ml-2 text-xs text-parchment-dim">experiment queue</span>
        </div>
        <div className="space-y-4 px-5 py-6 text-[13px] leading-relaxed">
          <p className="text-parchment-dim">
            <span className="text-signal-bright">user_id</span> · a3f2-91c...
          </p>
          <div className="rounded border border-ink-line bg-ink-panel px-3 py-2.5 text-parchment">
            "Summarize the drift in this week's eval results."
          </div>
          <p className="text-parchment-dim">
            queued on <span className="text-parchment">EXPERIMENT_QUEUE</span> — awaiting worker
          </p>
          <div className="flex items-center gap-2 text-signal-bright">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-signal" />
            sent successfully
          </div>
        </div>
      </div>
    </div>
  );
}
