from docker import DockerClient
from docker.errors import DockerException, ImageNotFound
from docker.models.containers import Container
import docker


class ExperimentRunnerClient:

    IMAGE = "experimentos/experiment-runner:latest"
    NETWORK = "experimentos-network"
    RUNNER_PORT = 9000


    def __init__(self, worker_id: str) -> None:

        self.client: DockerClient = docker.from_env()

        self.worker_id = worker_id
        self.container_name = f"experiment-runner-{worker_id}"

        self.container: Container | None = None


    def start(self) -> None:

        if self.container is not None:
            return

        try:
            self.client.images.get(self.IMAGE)

        except ImageNotFound as exc:
            raise RuntimeError(f"Runner image not found: {self.IMAGE}") from exc

        try:
            self.container = self.client.containers.create(
                image=self.IMAGE,
                name=self.container_name,

                command=["uvicorn", "runner:app", "--host", "0.0.0.0", "--port", str(self.RUNNER_PORT)],

                network=self.NETWORK,

                mem_limit="4g",
                nano_cpus=4_000_000_000,
                pids_limit=256,

                cap_drop=["ALL"],

                security_opt=["no-new-privileges:true"],

                read_only=True,

                tmpfs={ "/tmp": "rw,noexec,nosuid,size=512m" }
            )

            self.container.start()

        except DockerException as exc:

            self.container = None

            raise RuntimeError("Failed to create experiment runner container.") from exc


    def stop(self) -> None:

        if self.container is None:
            return

        try:
            if self.container.status == "running":
                self.container.stop(timeout=5)

        except DockerException:
            pass

        finally:
            try:
                self.container.remove(force=True)
            except DockerException:
                pass

            self.container = None


    @property
    def base_url(self) -> str:

        if self.container is None:
            raise RuntimeError("Experiment runner is not running.")

        return (f"http://{self.container_name}:{self.RUNNER_PORT}")


    def is_running(self) -> bool:

        if self.container is None:
            return False

        try:
            self.container.reload()
            return self.container.status == "running"

        except DockerException:
            return False