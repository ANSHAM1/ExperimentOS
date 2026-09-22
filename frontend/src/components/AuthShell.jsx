import { Link } from "react-router-dom";
import SignalVisual from "./SignalVisual";

export default function AuthShell({ eyebrow, title, subtitle, children }) {
  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[1fr_1fr]">
      <div className="flex items-center justify-center px-6 py-16 sm:px-10">
        <div className="w-full max-w-sm">
          <Link to="/" className="inline-flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-signal shadow-[0_0_10px_2px_rgba(255,90,31,0.55)]" />
            <span className="font-serif text-[21px] tracking-tight text-parchment">Signal</span>
          </Link>

          <div className="mt-10">
            <p className="text-[13.5px] text-signal-bright">{eyebrow}</p>
            <h1 className="mt-2 font-serif text-[32px] leading-tight text-parchment text-balance">
              {title}
            </h1>
            {subtitle && (
              <p className="mt-3 text-[15px] leading-relaxed text-parchment-dim">{subtitle}</p>
            )}
          </div>

          <div className="mt-8">{children}</div>
        </div>
      </div>

      <div className="relative hidden overflow-hidden border-l border-ink-line bg-ink-panel bg-grain lg:block">
        <SignalVisual />
        <div className="absolute bottom-10 left-1/2 w-full max-w-xs -translate-x-1/2 px-6 text-center">
          <p className="text-[13px] leading-relaxed text-parchment-faint">
            Your agent reaches Postgres, MySQL, MongoDB and Redis the moment you connect them —
            no redeploys.
          </p>
        </div>
      </div>
    </div>
  );
}
