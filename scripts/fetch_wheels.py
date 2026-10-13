"""Baixa wheels do PyPI usando curl, para máquinas onde o TLS do Python falha em files.pythonhosted.org.

Resolve as dependências (transitivas) pela API JSON do pypi.org, escolhe a maior versão que satisfaz os
requisitos e tem wheel compatível com Windows x64 / CPython 3.12, e baixa os arquivos com curl para uma pasta
("wheelhouse"). Depois instale com:

    pip install --no-index --find-links wheelhouse -r requirements-rufas.txt

Uso:
    python scripts/fetch_wheels.py wheelhouse "numpy==2.2.0" "scipy>=1.15.1" ...
"""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

from pip._vendor.packaging import tags
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.utils import canonicalize_name, parse_wheel_filename
from pip._vendor.packaging.version import InvalidVersion, Version

ENV = {
    "python_version": "3.12",
    "python_full_version": "3.12.10",
    "sys_platform": "win32",
    "platform_system": "Windows",
    "os_name": "nt",
    "platform_machine": "AMD64",
    "implementation_name": "cpython",
    "platform_python_implementation": "CPython",
    "extra": "",
}
SUPPORTED_TAGS = list(tags.cpython_tags((3, 12), platforms=["win_amd64"])) + list(
    tags.compatible_tags((3, 12), interpreter="cp312", platforms=["win_amd64"])
)
TAG_RANK = {tag: rank for rank, tag in enumerate(SUPPORTED_TAGS)}


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def pick_wheel(files: list[dict]) -> dict | None:
    best, best_rank = None, None
    for file in files:
        name = file["filename"]
        if not name.endswith(".whl") or file.get("yanked"):
            continue
        try:
            _, _, _, file_tags = parse_wheel_filename(name)
        except Exception:
            continue
        ranks = [TAG_RANK[t] for t in file_tags if t in TAG_RANK]
        if ranks and (best_rank is None or min(ranks) < best_rank):
            best, best_rank = file, min(ranks)
    return best


def resolve(requirements: list[str]) -> dict[str, tuple[str, dict]]:
    chosen: dict[str, tuple[str, dict]] = {}
    queue = [Requirement(r) for r in requirements]
    specs: dict[str, list[Requirement]] = {}
    while queue:
        req = queue.pop(0)
        if req.marker and not req.marker.evaluate(ENV):
            continue
        key = canonicalize_name(req.name)
        specs.setdefault(key, []).append(req)
        if key in chosen:
            version, _ = chosen[key]
            if all(r.specifier.contains(version, prereleases=True) for r in specs[key]):
                continue
        project = get_json(f"https://pypi.org/pypi/{key}/json")
        candidates: list[Version] = []
        for v in project["releases"]:
            try:
                parsed = Version(v)
            except InvalidVersion:
                continue
            if parsed.is_prerelease or parsed.is_devrelease:
                continue
            if all(r.specifier.contains(parsed) for r in specs[key]):
                candidates.append(parsed)
        for version in sorted(candidates, reverse=True):
            release = get_json(f"https://pypi.org/pypi/{key}/{version}/json")
            wheel = pick_wheel(release["urls"])
            if wheel is None:
                continue
            chosen[key] = (str(version), wheel)
            for dep in release["info"].get("requires_dist") or []:
                queue.append(Requirement(dep))
            break
        else:
            raise SystemExit(f"Nenhuma versão compatível de {key} para {[str(r) for r in specs[key]]}")
    return chosen


def main() -> None:
    target = Path(sys.argv[1])
    target.mkdir(parents=True, exist_ok=True)
    chosen = resolve(sys.argv[2:])
    for key, (version, wheel) in sorted(chosen.items()):
        destination = target / wheel["filename"]
        if destination.exists():
            print(f"ok      {wheel['filename']}")
            continue
        print(f"baixa   {wheel['filename']}")
        subprocess.run(["curl", "-sSL", "--fail", "-o", str(destination), wheel["url"]], check=True)
    print(f"\n{len(chosen)} pacotes em {target}")


if __name__ == "__main__":
    main()
