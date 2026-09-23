import { useEffect, useState } from "react";
import Modal from "./Modal";
import Field from "./Field";
import Button from "./Button";
import { DB_TYPES, getDbType } from "../store/dbTypes";

const EMPTY_FORM = {
  name: "",
  host: "",
  port: "",
  database: "",
  username: "",
  password: "",
  ssl: false,
  uri: "",
  filePath: "",
};

export default function ConnectDatabaseModal({ open, onClose, initialTypeId, onSubmit }) {
  const [typeId, setTypeId] = useState(initialTypeId || "postgresql");
  const [useUri, setUseUri] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const type = getDbType(typeId);

  useEffect(() => {
    if (open) {
      setTypeId(initialTypeId || "postgresql");
      setUseUri(false);
      setForm({ ...EMPTY_FORM, port: getDbType(initialTypeId || "postgresql").defaultPort || "" });
      setError("");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, initialTypeId]);

  function selectType(id) {
    setTypeId(id);
    setUseUri(false);
    setForm({ ...EMPTY_FORM, port: getDbType(id).defaultPort || "" });
    setError("");
  }

  function handleClose() {
    setForm(EMPTY_FORM);
    setUseUri(false);
    setError("");
    onClose();
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const payload = {
        type: typeId,
        name: form.name.trim() || type.label,
        ssl: form.ssl,
      };

      if (type.fileBased) {
        payload.database = form.filePath.trim();
      } else if (useUri && type.supportsUri) {
        payload.uri = form.uri.trim();
      } else {
        payload.host = form.host.trim();
        payload.port = form.port ? Number(form.port) : type.defaultPort;
        if (type.hasDatabase) payload.database = form.database.trim();
        if (type.hasUsername) {
          payload.username = form.username.trim();
          payload.password = form.password;
        } else {
          payload.password = form.password;
        }
      }

      await onSubmit(payload);
      handleClose();
    } catch (err) {
      setError(err.message || "Couldn't connect. Check the details and try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal
      open={open}
      onClose={handleClose}
      title="Connect a database"
      subtitle="Your agent will use this connection to read and query data."
    >
      <div className="mb-5 flex flex-wrap gap-1.5">
        {DB_TYPES.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => selectType(t.id)}
            className={`rounded-full border px-3 py-1.5 text-[13px] transition-colors ${
              t.id === typeId
                ? "border-signal-dim bg-signal-wash text-signal-bright"
                : "border-ink-line text-parchment-dim hover:border-ink-line-strong hover:text-parchment"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Field
          label="Connection name"
          placeholder={`e.g. ${type.label} — production`}
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        {type.fileBased ? (
          <Field
            label="File path"
            placeholder="/data/app.sqlite3"
            required
            value={form.filePath}
            onChange={(e) => setForm({ ...form, filePath: e.target.value })}
          />
        ) : (
          <>
            {type.supportsUri && (
              <button
                type="button"
                onClick={() => setUseUri((v) => !v)}
                className="text-[13px] text-parchment-dim underline decoration-ink-line-strong underline-offset-4 hover:text-parchment"
              >
                {useUri ? "Enter fields individually instead" : "Paste a connection string instead"}
              </button>
            )}

            {useUri ? (
              <Field
                label="Connection string"
                placeholder={type.uriPlaceholder}
                required
                className="font-mono"
                value={form.uri}
                onChange={(e) => setForm({ ...form, uri: e.target.value })}
              />
            ) : (
              <>
                <div className="grid grid-cols-[1fr_120px] gap-3">
                  <Field
                    label="Host"
                    placeholder="127.0.0.1"
                    required
                    value={form.host}
                    onChange={(e) => setForm({ ...form, host: e.target.value })}
                  />
                  <Field
                    label="Port"
                    inputMode="numeric"
                    placeholder={String(type.defaultPort)}
                    value={form.port}
                    onChange={(e) => setForm({ ...form, port: e.target.value })}
                  />
                </div>

                {type.hasDatabase && (
                  <Field
                    label="Database name"
                    required
                    value={form.database}
                    onChange={(e) => setForm({ ...form, database: e.target.value })}
                  />
                )}

                <div className="grid grid-cols-2 gap-3">
                  {type.hasUsername && (
                    <Field
                      label="Username"
                      autoComplete="off"
                      value={form.username}
                      onChange={(e) => setForm({ ...form, username: e.target.value })}
                    />
                  )}
                  <Field
                    label="Password"
                    type="password"
                    autoComplete="off"
                    className={type.hasUsername ? "" : "col-span-2"}
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                  />
                </div>
              </>
            )}

            <label className="flex items-center gap-2 text-[13.5px] text-parchment-dim">
              <input
                type="checkbox"
                checked={form.ssl}
                onChange={(e) => setForm({ ...form, ssl: e.target.checked })}
                className="h-3.5 w-3.5 rounded border-ink-line-strong bg-ink-raised text-signal accent-signal"
              />
              Require SSL/TLS
            </label>
          </>
        )}

        {error && <p className="text-[13px] text-flag">{error}</p>}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="ghost" onClick={handleClose}>
            Cancel
          </Button>
          <Button type="submit" loading={submitting}>
            Connect
          </Button>
        </div>
      </form>
    </Modal>
  );
}
