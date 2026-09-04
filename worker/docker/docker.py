import docker

from docker import DockerClient
from docker.errors import DockerException
from docker.models.containers import Container


class DockerContainerClient:

    IMAGE = "script-runner:latest"

    def __init__(self) -> None:

        self.client: DockerClient = docker.from_env()


    def run(self, experiment_directory: str, *, timeout: int = 300) -> tuple[int, str, str]:

        container: Container | None = None

        try:

            container = self.client.containers.create(
                image=self.IMAGE,

                command=[
                    "python",
                    "/experiment/main.py",
                ],

                volumes={
                    experiment_directory: {
                        "bind": "/experiment",
                        "mode": "rw",
                    },
                },

                network_mode="none",

                mem_limit="2g",
                nano_cpus=2_000_000_000,
                pids_limit=128,

                read_only=True,

                cap_drop=[
                    "ALL",
                ],

                security_opt=[
                    "no-new-privileges:true",
                ],

                user="10001:10001",

                name=None
            )

            container.start()

            result = container.wait(timeout=timeout)

            status_code = int(result["StatusCode"])

            stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")

            stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")

            return (status_code, stdout, stderr)

        except Exception:

            if container is not None:

                try:
                    container.kill()
                except DockerException:
                    pass

            raise

        finally:

            if container is not None:

                try:
                    container.remove(
                        force=True,
                    )
                except DockerException:
                    pass