import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { experimentApi } from "../lib/apiClient";
import Button from "../components/Button";

export default function ConsolePage() {
  const { logout } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [log, setLog] = useState([]);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setError("");
    setSubmitting(true);
    const sent = prompt.trim();
    try {
      const data = await experimentApi.run(sent);
      setLog((prev) => [{ prompt: sent, output: data?.output || "No response", at: new Date() }, ...prev]);
      setPrompt("");
    } catch {
      setError("The request didn't go through. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-ink">
      <header className="flex items-center justify-between border-b border-ink-line px-6 py-4 sm:px-10">
        <span className="font-serif text-xl text-parchment">Signal</span>
        <button
          onClick={logout}
          className="text-[14px] text-parchment-dim transition-colors hover:text-parchment"
        >
          Sign out
        </button>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-16 sm:px-10">
        <h1 className="font-serif text-3xl text-parchment">Run an experiment</h1>
        <p className="mt-2 text-[15px] text-parchment-dim">
          Prompts are queued to your agent workflow and processed asynchronously.
        </p>

        <form onSubmit={handleSubmit} className="mt-8">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe what you want the agent to do…"
            rows={4}
            className="w-full resize-none rounded-md border border-ink-line bg-ink-panel px-3.5 py-3 text-[15px] text-parchment placeholder:text-parchment-dim/60 transition-colors focus:border-signal-dim"
          />
          {error && <p className="mt-2 text-[13px] text-flag">{error}</p>}
          <div className="mt-3 flex justify-end">
            <div className="w-40">
              <Button type="submit" loading={submitting} disabled={!prompt.trim()}>
                Send prompt
              </Button>
            </div>
          </div>
        </form>

        {log.length > 0 && (
          <ul className="mt-10 space-y-3">
            {log.map((entry, i) => (
              <li key={i} className="rounded-md border border-ink-line bg-ink-panel px-4 py-3.5">
                <p className="text-[15px] text-parchment">{entry.prompt}</p>
                <p className="mt-1.5 text-[13px] text-signal-bright">{entry.output}</p>
                <p className="mt-1 text-[12px] text-parchment-dim">
                  {entry.at.toLocaleTimeString()}
                </p>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
