"""Execução em segundo plano das simulações do RuFaS disparadas pela interface web."""

from __future__ import annotations

import threading
import time
import traceback
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

# Cada simulação do RuFaS usa ~1,2 GB de RAM. Só um job por vez (cada job pode usar até 2 simulações em paralelo).
_RUN_LOCK = threading.Lock()


class Cancelled(Exception):
    """O trabalho foi cancelado a pedido do usuário (o job termina com o estado ``cancelled``)."""


@dataclass
class Job:
    id: str
    kind: str
    params: dict[str, Any]
    status: str = "queued"  # queued | running | done | error | cancelled
    cancel_requested: bool = False
    done: int = 0
    total: int = 0
    result: Any = None
    error: str = ""
    created: float = field(default_factory=time.time)
    finished: float | None = None

    def public(self, include_result: bool = True) -> dict[str, Any]:
        data = {
            "id": self.id,
            "kind": self.kind,
            "status": self.status,
            "done": self.done,
            "total": self.total,
            "error": self.error,
            "created": self.created,
            "finished": self.finished,
        }
        if include_result:
            data["result"] = self.result
        return data


class JobManager:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}

    def submit(self, kind: str, params: dict[str, Any], work: Callable[[Job], Any]) -> Job:
        job = Job(id=uuid.uuid4().hex[:10], kind=kind, params=params)
        self._jobs[job.id] = job
        threading.Thread(target=self._run, args=(job, work), daemon=True).start()
        return job

    def _run(self, job: Job, work: Callable[[Job], Any]) -> None:
        with _RUN_LOCK:
            if job.cancel_requested:  # cancelado ainda na fila
                job.status, job.finished = "cancelled", time.time()
                return
            job.status = "running"
            try:
                job.result = work(job)
                job.status = "done"
            except Cancelled:
                job.status = "cancelled"
            except Exception as exc:  # noqa: BLE001 - qualquer falha vai para a interface
                job.status = "error"
                job.error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=4)}"
            finally:
                job.finished = time.time()

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def cancel(self, job_id: str) -> Job | None:
        """Pede o cancelamento: o trabalho para na próxima verificação (``cancel_requested``); um job na fila nem começa."""
        job = self._jobs.get(job_id)
        if job and job.status in ("queued", "running"):
            job.cancel_requested = True
        return job

    def list(self) -> list[dict[str, Any]]:
        return [j.public(include_result=False) for j in sorted(self._jobs.values(), key=lambda j: -j.created)]
