import asyncio
import os
import sys
import tempfile

from pathlib import Path


class PythonExecutor:

    def __init__(self, timeout: int = 300) -> None:
        
        self.timeout = timeout


    async def execute(self, experiment_id: str, code: str) -> tuple[int, str, str]:

        with tempfile.TemporaryDirectory(prefix=f"experiment-{experiment_id}-") as directory:

            experiment_dir = Path(directory)

            script_path = experiment_dir / "main.py"

            script_path.write_text(code, encoding="utf-8")

            process = await asyncio.create_subprocess_exec(
                sys.executable,
                str(script_path),

                cwd=str(experiment_dir),

                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,

                env={
                    "PATH": os.environ.get("PATH", ""),
                    "PYTHONUNBUFFERED": "1",
                },
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)

            except asyncio.TimeoutError:

                process.kill()

                await process.wait()

                return (-1, "", "Execution timed out.")

            return (
                process.returncode or 0,
                stdout.decode(
                    "utf-8",
                    errors="replace",
                ),
                stderr.decode(
                    "utf-8",
                    errors="replace",
                ),
            )