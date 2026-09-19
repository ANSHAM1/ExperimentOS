import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AuthShell from "../components/AuthShell";
import Field from "../components/Field";
import Button from "../components/Button";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const result = await login(form.email.trim(), form.password);
      if (!result.success) {
        setError(result.message);
        return;
      }
      navigate("/console", { replace: true });
    } catch {
      setError("Couldn't reach the server. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      eyebrow="Welcome back"
      title="Sign in to your console"
      subtitle="Your session stays open across tabs and restarts until it expires — no need to sign in every visit."
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field
          label="Email"
          type="email"
          required
          autoComplete="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <Field
          label="Password"
          type="password"
          required
          autoComplete="current-password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {error && <p className="text-[13px] text-flag">{error}</p>}
        <Button type="submit" loading={submitting}>
          Sign in
        </Button>
      </form>
      <p className="mt-6 text-[14px] text-parchment-dim">
        New here?{" "}
        <Link to="/register" className="text-parchment underline underline-offset-4">
          Create an account
        </Link>
      </p>
    </AuthShell>
  );
}
