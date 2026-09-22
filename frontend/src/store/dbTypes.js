// Central registry of supported database engines. Add an entry here to add
// a new engine to the "Connect a database" grid — everything else (the
// tile, the form fields, the default port) is derived from this list.
export const DB_TYPES = [
  {
    id: "postgresql",
    label: "PostgreSQL",
    short: "PG",
    accent: "#5A9BD8",
    defaultPort: 5432,
    hasDatabase: true,
    hasUsername: true,
    supportsUri: true,
    uriPlaceholder: "postgresql://user:pass@host:5432/dbname",
  },
  {
    id: "mysql",
    label: "MySQL",
    short: "SQL",
    accent: "#E2A33C",
    defaultPort: 3306,
    hasDatabase: true,
    hasUsername: true,
    supportsUri: true,
    uriPlaceholder: "mysql://user:pass@host:3306/dbname",
  },
  {
    id: "mongodb",
    label: "MongoDB",
    short: "MDB",
    accent: "#5FBF88",
    defaultPort: 27017,
    hasDatabase: true,
    hasUsername: true,
    supportsUri: true,
    uriPlaceholder: "mongodb+srv://user:pass@cluster.mongodb.net/dbname",
  },
  {
    id: "redis",
    label: "Redis",
    short: "RDS",
    accent: "#FF5A1F",
    defaultPort: 6379,
    hasDatabase: false,
    hasUsername: false,
    supportsUri: true,
    uriPlaceholder: "redis://default:pass@host:6379",
  },
  {
    id: "mssql",
    label: "SQL Server",
    short: "TDS",
    accent: "#8B7CD8",
    defaultPort: 1433,
    hasDatabase: true,
    hasUsername: true,
    supportsUri: false,
  },
  {
    id: "sqlite",
    label: "SQLite",
    short: "LITE",
    accent: "#A79689",
    fileBased: true,
    hasDatabase: false,
    hasUsername: false,
    supportsUri: false,
  },
];

export function getDbType(id) {
  return DB_TYPES.find((t) => t.id === id) || DB_TYPES[0];
}
