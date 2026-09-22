const NODES = [
  { label: "PG", angle: -55, kind: "postgresql" },
  { label: "SQL", angle: 35, kind: "mysql" },
  { label: "MDB", angle: 125, kind: "mongodb" },
  { label: "RDS", angle: -145, kind: "redis" },
];

const CENTER = { x: 210, y: 210 };
const RADIUS = 148;

function point(angleDeg) {
  const rad = (angleDeg * Math.PI) / 180;
  return {
    x: CENTER.x + RADIUS * Math.cos(rad),
    y: CENTER.y + RADIUS * Math.sin(rad),
  };
}

export default function SignalVisual() {
  return (
    <div className="relative flex h-full w-full items-center justify-center">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage:
            "linear-gradient(to right, #F4EEE4 1px, transparent 1px), linear-gradient(to bottom, #F4EEE4 1px, transparent 1px)",
          backgroundSize: "34px 34px",
        }}
      />

      <svg viewBox="0 0 420 420" className="relative w-full max-w-md">
        <defs>
          <radialGradient id="agentGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF5A1F" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#FF5A1F" stopOpacity="0" />
          </radialGradient>
        </defs>

        {NODES.map((node) => {
          const p = point(node.angle);
          const midX = (CENTER.x + p.x) / 2 + (p.y - CENTER.y) * 0.08;
          const midY = (CENTER.y + p.y) / 2 - (p.x - CENTER.x) * 0.08;
          return (
            <path
              key={node.kind}
              d={`M ${CENTER.x} ${CENTER.y} Q ${midX} ${midY} ${p.x} ${p.y}`}
              fill="none"
              stroke="#3B2F25"
              strokeWidth="1.5"
            />
          );
        })}

        {NODES.map((node, i) => {
          const p = point(node.angle);
          const midX = (CENTER.x + p.x) / 2 + (p.y - CENTER.y) * 0.08;
          const midY = (CENTER.y + p.y) / 2 - (p.x - CENTER.x) * 0.08;
          return (
            <path
              key={`flow-${node.kind}`}
              d={`M ${CENTER.x} ${CENTER.y} Q ${midX} ${midY} ${p.x} ${p.y}`}
              fill="none"
              stroke="#FF8A4C"
              strokeWidth="1.5"
              strokeDasharray="3 9"
              opacity="0.8"
            >
              <animate
                attributeName="stroke-dashoffset"
                from="0"
                to="-24"
                dur="1.6s"
                begin={`${i * 0.25}s`}
                repeatCount="indefinite"
              />
            </path>
          );
        })}

        <circle cx={CENTER.x} cy={CENTER.y} r="70" fill="url(#agentGlow)" />
        <circle
          cx={CENTER.x}
          cy={CENTER.y}
          r="30"
          fill="none"
          stroke="#FF5A1F"
          strokeWidth="1"
          opacity="0.5"
          className="origin-center animate-pulse-ring"
        />
        <circle cx={CENTER.x} cy={CENTER.y} r="26" fill="#1C1713" stroke="#FF5A1F" strokeWidth="1.5" />
        <text
          x={CENTER.x}
          y={CENTER.y + 5}
          textAnchor="middle"
          fontFamily="'JetBrains Mono', monospace"
          fontSize="11"
          fill="#F4EEE4"
        >
          agent
        </text>

        {NODES.map((node) => {
          const p = point(node.angle);
          return (
            <g key={`node-${node.kind}`}>
              <circle cx={p.x} cy={p.y} r="21" fill="#1C1713" stroke="#3B2F25" strokeWidth="1.5" />
              <text
                x={p.x}
                y={p.y + 4}
                textAnchor="middle"
                fontFamily="'JetBrains Mono', monospace"
                fontSize="10"
                fill="#A79689"
              >
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
