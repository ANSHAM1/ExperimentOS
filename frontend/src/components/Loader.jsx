export default function Loader() {
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-ink">
      <div className="relative h-8 w-8">
        <span className="absolute inset-0 rounded-full border-2 border-ink-line" />
        <span className="absolute inset-0 rounded-full border-2 border-transparent border-t-signal animate-spin" />
      </div>
    </div>
  );
}
