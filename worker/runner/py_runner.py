import asyncio
import os
import signal
import sys
import tempfile

from pathlib import Path


class Python:

    @staticmethod
    async def execute(experiment_id: str, code: str, timeout: int) -> tuple[int, str, str]:

        with tempfile.TemporaryDirectory(prefix=f"experiment-{experiment_id}-") as directory:

            experiment_dir = Path(directory)

            script_path = experiment_dir / "main.py"

            script_path.write_text(code, encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"

            process = await asyncio.create_subprocess_exec(
                sys.executable,
                str(script_path),

                cwd=str(experiment_dir),

                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,

                env=env,

                start_new_session=True,
            )

            try:

                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

            except asyncio.TimeoutError:

                try:

                    kill_signal = getattr(signal, "SIGKILL", signal.SIGTERM)

                    killpg = getattr(os, "killpg", None)

                    if killpg is not None:
                        killpg(process.pid, kill_signal)

                    else:
                        os.kill(process.pid, kill_signal)

                except ProcessLookupError:
                    pass

                await process.wait()

                return (-1, "", "Execution timed out.")

            return (
                process.returncode if process.returncode is not None else -1,
                stdout.decode("utf-8", errors="replace"),
                stderr.decode("utf-8", errors="replace")
            )