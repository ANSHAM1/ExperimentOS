# ExperimentOS
A distributed platform for defining, executing, monitoring, and analyzing long-running ML experiments.


                                Auth API
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
                Register                    Login
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                            AuthService
                                 │
                    ┌────────────┼─────────────┐
                    ▼            ▼             ▼
            UserRepository  PasswordHasher  SessionStore
                    │            │             │
                    ▼            ▼             ▼
                PostgreSQL    Argon2         Redis
                                │
                                ▼
                          Token Service
                                │
                                ▼
                               JWT