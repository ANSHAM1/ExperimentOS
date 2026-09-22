import { useRef } from "react";

export default function OtpInput({ length = 6, value, onChange }) {
  const inputsRef = useRef([]);
  const digits = value.split("").concat(Array(length).fill("")).slice(0, length);

  function setDigit(index, char) {
    const next = digits.slice();
    next[index] = char;
    onChange(next.join(""));
  }

  function handleChange(index, e) {
    const raw = e.target.value.replace(/\D/g, "");
    if (!raw) {
      setDigit(index, "");
      return;
    }
    const chars = raw.split("");
    const next = digits.slice();
    let cursor = index;
    for (const ch of chars) {
      if (cursor >= length) break;
      next[cursor] = ch;
      cursor += 1;
    }
    onChange(next.join(""));
    const focusIndex = Math.min(cursor, length - 1);
    inputsRef.current[focusIndex]?.focus();
  }

  function handleKeyDown(index, e) {
    if (e.key === "Backspace" && !digits[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
    if (e.key === "ArrowLeft" && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
    if (e.key === "ArrowRight" && index < length - 1) {
      inputsRef.current[index + 1]?.focus();
    }
  }

  function handlePaste(e) {
    const text = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, length);
    if (!text) return;
    e.preventDefault();
    onChange(text);
    const focusIndex = Math.min(text.length, length - 1);
    inputsRef.current[focusIndex]?.focus();
  }

  return (
    <div className="flex gap-2" onPaste={handlePaste}>
      {digits.map((digit, i) => (
        <input
          key={i}
          ref={(el) => (inputsRef.current[i] = el)}
          value={digit}
          onChange={(e) => handleChange(i, e)}
          onKeyDown={(e) => handleKeyDown(i, e)}
          onFocus={(e) => e.target.select()}
          inputMode="numeric"
          maxLength={1}
          className="h-12 w-full rounded-lg border border-ink-line bg-ink-raised text-center font-mono text-[19px] text-parchment transition-colors focus:border-signal-dim"
        />
      ))}
    </div>
  );
}
