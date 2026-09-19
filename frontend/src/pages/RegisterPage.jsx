import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AuthShell from "../components/AuthShell";
import Field from "../components/Field";
import Button from "../components/Button";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const result = await register(form.email.trim(), form.password);
      if (!result.success) {
        setError(result.message || "Registration failed");
        return;
      }
      navigate("/verify", { state: { email: form.email.trim() }, replace: true });
    } catch {
      setError("Couldn't reach the server. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      eyebrow="Get started"
      title="Create your account"
      subtitle="We'll send a one-time code to confirm your email before your account goes live."
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
          minLength={8}
          autoComplete="new-password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {error && <p className="text-[13px] text-flag">{error}</p>}
        <Button type="submit" loading={submitting}>
          Create account
        </Button>
      </form>
      <p className="mt-6 text-[14px] text-parchment-dim">
        Already have an account?{" "}
        <Link to="/login" className="text-parchment underline underline-offset-4">
          Sign in
        </Link>
      </p>
    </AuthShell>
  );
}
