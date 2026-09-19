import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AuthShell from "../components/AuthShell";
import Field from "../components/Field";
import Button from "../components/Button";

export default function VerifyPage() {
  const { verifyEmail } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || "");
  const [otp, setOtp] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const result = await verifyEmail(email.trim(), otp.trim());
      if (!result.success) {
        setError(result.message || "That code didn't work");
        return;
      }
      setDone(true);
    } catch {
      setError("Couldn't reach the server. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (done) {
    return (
      <AuthShell eyebrow="All set" title="Email verified" subtitle="Your account is ready to use.">
        <Link to="/login">
          <Button type="button">Continue to sign in</Button>
        </Link>
      </AuthShell>
    );
  }

  return (
    <AuthShell
      eyebrow="Check your inbox"
      title="Enter your code"
      subtitle="We sent a 6-digit code to your email. It expires in 10 minutes."
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field
          label="Email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          label="Verification code"
          type="text"
          inputMode="numeric"
          required
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
        {error && <p className="text-[13px] text-flag">{error}</p>}
        <Button type="submit" loading={submitting}>
          Verify email
        </Button>
      </form>
    </AuthShell>
  );
}
