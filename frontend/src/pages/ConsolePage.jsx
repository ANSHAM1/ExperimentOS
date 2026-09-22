import { useEffect, useState } from "react";
import { Plug, Send } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { experimentApi, integrationsApi } from "../api/apiClient";
import { DB_TYPES } from "../lib/dbTypes";
import Button from "../components/Button";
import DatabaseTypeCard from "../components/DatabaseTypeCard";
import DatabaseRow from "../components/DatabaseRow";
import ConnectDatabaseModal from "../components/ConnectDatabaseModal";

export default function ConsolePage() {
  const { logout, email } = useAuth();
  const toast = useToast();

  const [databases, setDatabases] = useState([]);
  const [loadingDbs, setLoadingDbs] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [pendingType, setPendingType] = useState("postgresql");

  const [prompt, setPrompt] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [log, setLog] = useState([]);
  const [promptError, setPromptError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await integrationsApi.list();
        setDatabases(data?.databases || []);
      } catch {
        // Integration endpoints may not be wired up on the backend yet —
        // fail quietly on the initial load and keep the empty state.
        setDatabases([]);
      } finally {
        setLoadingDbs(false);
      }
    })();
  }, []);

  function openModalFor(typeId) {
    setPendingType(typeId);
    setModalOpen(true);
  }

  async function handleCreate(payload) {
    const data = await integrationsApi.create(payload);
    if (!data?.success) {
      throw new Error(data?.message || "Couldn't connect. Check the details and try again.");
    }
    setDatabases((prev) => [data.database, ...prev]);
    toast.success(`${data.database?.name || payload.name} connected.`);
  }

  async function handleTest(id) {
    try {
      const data = await integrationsApi.test(id);
      setDatabases((prev) =>
        prev.map((d) => (d.id === id ? { ...d, status: data?.status || (data?.success ? "connected" : "error") } : d)),
      );
      if (data?.success) {
        toast.success("Connection is healthy.");
      } else {
        toast.error(data?.message || "Connection test failed.");
      }
    } catch (err) {
      setDatabases((prev) => prev.map((d) => (d.id === id ? { ...d, status: "error" } : d)));
      toast.error(err.message || "Connection test failed.");
    }
  }

  async function handleRemove(id) {
    const previous = databases;
    setDatabases((prev) => prev.filter((d) => d.id !== id));
    try {
      await integrationsApi.remove(id);
      toast.success("Connection removed.");
    } catch (err) {
      setDatabases(previous);
      toast.error(err.message || "Couldn't remove that connection.");
    }
  }

  async function handleSubmitPrompt(e) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setPromptError("");
    setSubmitting(true);
    const sent = prompt.trim();
    try {
      const data = await experimentApi.run(sent);
      setLog((prev) => [{ prompt: sent, output: data?.output || "No response", at: new Date() }, ...prev]);
      setPrompt("");
    } catch {
      setPromptError("The request didn't go through. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-ink">
      <header className="flex items-center justify-between border-b border-ink-line px-6 py-4 sm:px-10">
        <span className="inline-flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-signal shadow-[0_0_10px_2px_rgba(255,90,31,0.55)]" />
          <span className="font-serif text-lg text-parchment">Signal</span>
        </span>
        <div className="flex items-center gap-4">
          {email && <span className="hidden text-[13.5px] text-parchment-faint sm:inline">{email}</span>}
          <button
            onClick={logout}
            className="text-[14px] text-parchment-dim transition-colors hover:text-parchment"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-14 sm:px-10">
        <section>
          <h1 className="font-serif text-[28px] text-parchment">Connect a database</h1>
          <p className="mt-2 text-[15px] leading-relaxed text-parchment-dim">
            Link a database so your agent can read and query it directly during experiments.
          </p>

          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
            {DB_TYPES.map((type) => (
              <DatabaseTypeCard key={type.id} type={type} onClick={() => openModalFor(type.id)} />
            ))}
          </div>

          <div className="mt-8">
            {loadingDbs ? (
              <div className="space-y-2">
                {[0, 1].map((i) => (
                  <div key={i} className="h-[60px] animate-pulse rounded-xl border border-ink-line bg-ink-panel" />
                ))}
              </div>
            ) : databases.length === 0 ? (
              <div className="flex flex-col items-start gap-2 rounded-xl border border-dashed border-ink-line px-5 py-6">
                <Plug className="h-[18px] w-[18px] text-parchment-faint" />
                <p className="text-[14px] text-parchment-dim">
                  No databases connected yet. Choose an engine above to get started.
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {databases.map((db) => (
                  <DatabaseRow key={db.id} db={db} onTest={handleTest} onRemove={handleRemove} />
                ))}
              </div>
            )}
          </div>
        </section>

        <div className="my-14 h-px bg-ink-line" />

        <section>
          <h2 className="font-serif text-2xl text-parchment">Run an experiment</h2>
          <p className="mt-2 text-[15px] text-parchment-dim">
            Prompts are queued to your agent workflow and processed asynchronously.
          </p>

          <form onSubmit={handleSubmitPrompt} className="mt-6">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe what you want the agent to do…"
              rows={4}
              className="w-full resize-none rounded-lg border border-ink-line bg-ink-raised px-3.5 py-3 text-[15px] text-parchment placeholder:text-parchment-faint transition-colors focus:border-signal-dim"
            />
            {promptError && <p className="mt-2 text-[13px] text-flag">{promptError}</p>}
            <div className="mt-3 flex justify-end">
              <Button type="submit" loading={submitting} disabled={!prompt.trim()}>
                <Send className="h-3.5 w-3.5" />
                Send prompt
              </Button>
            </div>
          </form>

          {log.length > 0 && (
            <ul className="mt-8 space-y-2.5">
              {log.map((entry, i) => (
                <li key={i} className="rounded-lg border border-ink-line bg-ink-panel px-4 py-3.5">
                  <p className="text-[15px] text-parchment">{entry.prompt}</p>
                  <p className="mt-1.5 text-[13px] text-signal-bright">{entry.output}</p>
                  <p className="mt-1 text-[12px] text-parchment-faint">{entry.at.toLocaleTimeString()}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>

      <ConnectDatabaseModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        initialTypeId={pendingType}
        onSubmit={handleCreate}
      />
    </div>
  );
}
