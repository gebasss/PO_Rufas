"""Cancelamento de tarefas em segundo plano (RF-30: a otimização leva alguns segundos)."""

import threading
import time

from dietopt.jobs import Cancelled, JobManager


def esperar(job, estados, limite=5.0):
    fim = time.time() + limite
    while job.status not in estados and time.time() < fim:
        time.sleep(0.01)
    return job.status


def test_job_cancelado_durante_a_execucao_termina_como_cancelled():
    manager = JobManager()
    iniciou = threading.Event()

    def trabalho(job):
        iniciou.set()
        while not job.cancel_requested:
            time.sleep(0.005)
        raise Cancelled

    job = manager.submit("teste", {}, trabalho)
    assert iniciou.wait(5)
    assert manager.cancel(job.id) is job
    assert esperar(job, {"cancelled", "done", "error"}) == "cancelled"
    assert job.finished is not None and job.error == ""


def test_job_cancelado_na_fila_nem_comeca():
    manager = JobManager()
    liberar = threading.Event()
    executou = []
    primeiro = manager.submit("primeiro", {}, lambda job: liberar.wait(5))
    segundo = manager.submit("segundo", {}, lambda job: executou.append(True))
    manager.cancel(segundo.id)
    liberar.set()
    assert esperar(segundo, {"cancelled", "done", "error"}) == "cancelled" and not executou
    assert esperar(primeiro, {"done", "error"}) == "done"


def test_cancelar_job_concluido_ou_inexistente_nao_muda_nada():
    manager = JobManager()
    job = manager.submit("rapido", {}, lambda job: 1)
    assert esperar(job, {"done"}) == "done"
    assert manager.cancel(job.id).cancel_requested is False
    assert manager.cancel("nao-existe") is None
