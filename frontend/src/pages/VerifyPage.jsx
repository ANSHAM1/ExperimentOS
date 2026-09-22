import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import AuthShell from "../components/AuthShell";
import Field from "../components/Field";
import OtpInput from "../components/OtpInput";
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
        <div className="mb-6 inline-flex items-center gap-2 rounded-lg border border-ok/25 bg-ok/10 px-3.5 py-2.5 text-[13.5px] text-ok">
          <CheckCircle2 className="h-4 w-4" />
          Verification complete
        </div>
        <Link to="/login" className="block">
          <Button type="button" className="w-full">
            Continue to sign in
          </Button>
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
      <form onSubmit={handleSubmit} className="space-y-5">
        <Field
          label="Email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <div>
          <span className="text-[13px] text-parchment-dim">Verification code</span>
          <div className="mt-1.5">
            <OtpInput value={otp} onChange={setOtp} />
          </div>
        </div>
        {error && <p className="text-[13px] text-flag">{error}</p>}
        <Button type="submit" loading={submitting} disabled={otp.length !== 6} className="w-full">
          Verify email
        </Button>
      </form>
      <p className="mt-6 text-[14px] text-parchment-dim">
        Wrong address?{" "}
        <Link to="/register" className="text-parchment underline decoration-ink-line-strong underline-offset-4 hover:decoration-signal">
          Start over
        </Link>
      </p>
    </AuthShell>
  );
}
