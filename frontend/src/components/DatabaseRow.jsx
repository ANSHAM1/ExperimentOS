import { useState } from "react";
import { Loader2, RefreshCw, Trash2 } from "lucide-react";
import { getDbType } from "../lib/dbTypes";
import StatusDot from "./StatusDot";

export default function DatabaseRow({ db, onTest, onRemove }) {
  const type = getDbType(db.type);
  const [testing, setTesting] = useState(false);
  const [removing, setRemoving] = useState(false);

  async function handleTest() {
    setTesting(true);
    try {
      await onTest(db.id);
    } finally {
      setTesting(false);
    }
  }

  async function handleRemove() {
    setRemoving(true);
    try {
      await onRemove(db.id);
    } catch {
      setRemoving(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-ink-line bg-ink-panel px-4 py-3.5 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-3">
        <span
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg font-mono text-[10px] font-medium"
          style={{ backgroundColor: `${type.accent}14`, color: type.accent }}
        >
          {type.short}
        </span>
        <div>
          <p className="text-[14.5px] text-parchment">{db.name}</p>
          <p className="font-mono text-[12px] text-parchment-faint">
            {db.uri ? db.uri : `${db.host}${db.port ? `:${db.port}` : ""}${db.database ? `/${db.database}` : ""}`}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <StatusDot status={testing ? "testing" : db.status} />
        <div className="flex items-center gap-1">
          <button
            onClick={handleTest}
            disabled={testing}
            className="rounded-md p-1.5 text-parchment-faint transition-colors hover:bg-ink-raised hover:text-parchment disabled:opacity-50"
            aria-label="Test connection"
          >
            {testing ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="h-4 w-4" />
            )}
          </button>
          <button
            onClick={handleRemove}
            disabled={removing}
            className="rounded-md p-1.5 text-parchment-faint transition-colors hover:bg-flag/10 hover:text-flag disabled:opacity-50"
            aria-label="Remove connection"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
