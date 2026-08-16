#!/usr/bin/env python3
"""Drift-check cross-repo per DataCivicLab.

Verifica che i repo dell'org usino i componenti condivisi del repository
`.github` e non reintroducano copie inline o versioni disallineate.

Risultati per severità:
  ERROR — bloccano il job (exit 1): roba che va migrata al componente condiviso.
  WARN  — disallineamenti minori, non bloccano (exit 0).

Casi verificati per ogni repo in scope:
  A. `test-audit.yml` deve referenziare il reusable (`test-audit-reusable.yml`),
     non duplicarne il contenuto inline.
  B. i workflow con `setup-python` inline dovrebbero usare l'action org
     `dataciviclab/.github/actions/python-setup`.
  C. le versioni di `actions/checkout`, `actions/setup-python` e
     `actions/upload-artifact` devono appartenere all'allowlist canonica.

Uso (locale):
  python scripts/drift_check.py [--token $GITHUB_TOKEN]

In CI (workflow `templates.yml`) il report viene anche scritto in
`$GITHUB_STEP_SUMMARY`.

Dipendenze: solo stdlib.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field

API = "https://api.github.com"
RAW_ACCEPT = "application/vnd.github.raw"

# Repo in scope per il drift-check: core pipeline + repo dataset.
# Aggiungere un repo quando adotta il modello del layer condiviso (ADR-001).
REPOS = [
    "toolkit",
    "lab-connectors",
    "source-observatory",
    "dataset-incubator",
    "data-explorer",
    "lab-dashboard",
    "agent-context-builder",
    "eurostat",
    "open-siope",
    "open-conto-annuale",
    "dcl-bologna",
    "italia-corpus",
]

# Versioni canoniche delle action di piattaforma (target da standardizzare).
# I componenti condivisi in questo repo devono allinearsi qui (ADR-001 §5).
CANONICAL = {
    "actions/checkout": "v7",
    "actions/setup-python": "v7",
    "actions/upload-artifact": "v7",
}

REUSABLE_TEST_AUDIT = "test-audit-reusable.yml"
ORG_ACTION_PYTHON_SETUP = "dataciviclab/.github/actions/python-setup"

USES_RE = re.compile(r"^\s*uses:\s*([^\s#@]+)@([^\s#]+)", re.M)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def api_headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dataciviclab-drift-check",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api(url: str, token: str | None) -> dict | list:
    req = urllib.request.Request(url, headers=api_headers(token))
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_workflows(repo: str, ref: str, token: str | None) -> dict[str, str]:
    """Restituisce {filename: contenuto} dei workflow del repo."""
    workflows: dict[str, str] = {}
    url = f"{API}/repos/dataciviclab/{repo}/contents/.github/workflows?ref={ref}"
    try:
        entries = api(url, token)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return workflows  # nessuna cartella workflow
        raise
    if not isinstance(entries, list):
        return workflows
    for entry in entries:
        if entry["type"] != "file" or not entry["name"].endswith((".yml", ".yaml")):
            continue
        raw_url = f"{API}/repos/dataciviclab/{repo}/contents/{entry['path']}?ref={ref}"
        req = urllib.request.Request(
            raw_url, headers={**api_headers(token), "Accept": RAW_ACCEPT}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            workflows[entry["name"]] = resp.read().decode("utf-8", "replace")
    return workflows


def default_branch(repo: str, token: str | None) -> str:
    data = api(f"{API}/repos/dataciviclab/{repo}", token)
    return str(data["default_branch"])


def check_test_audit(repo: str, workflows: dict[str, str], report: Report) -> None:
    for name, text in workflows.items():
        if name != "test-audit.yml":
            continue
        if REUSABLE_TEST_AUDIT not in text:
            report.errors.append(
                f"{repo}: .github/workflows/{name} è una copia inline — "
                f"chiama il reusable dataciviclab/.github/.github/workflows/{REUSABLE_TEST_AUDIT}"
            )


def check_inline_setup_python(
    repo: str, workflows: dict[str, str], report: Report
) -> None:
    for name, text in workflows.items():
        if ORG_ACTION_PYTHON_SETUP in text:
            continue  # usa già l'action org
        if re.search(r"actions/setup-python@", text):
            report.warnings.append(
                f"{repo}: {name}: setup-python inline — usa {ORG_ACTION_PYTHON_SETUP}"
            )


def check_action_versions(
    repo: str, workflows: dict[str, str], report: Report
) -> None:
    for name, text in workflows.items():
        for m in USES_RE.finditer(text):
            action, version = m.group(1), m.group(2)
            canonical = CANONICAL.get(action)
            if canonical and version != canonical:
                report.warnings.append(
                    f"{repo}: {name}: {action}@{version} "
                    f"(canonico: {action}@{canonical})"
                )


def render(report: Report) -> list[str]:
    lines = ["Drift-check: repo org vs componenti condivisi (.github)", ""]
    if not report.errors and not report.warnings:
        lines.append("✅ Nessun disallineamento.")
        return lines
    if report.errors:
        lines.append(f"❌ ERRORI ({len(report.errors)}) — bloccano il merge:")
        lines.extend(f"  - {e}" for e in report.errors)
        lines.append("")
    if report.warnings:
        lines.append(f"⚠️ WARNING ({len(report.warnings)}) — non bloccano:")
        lines.extend(f"  - {w}" for w in report.warnings)
        lines.append("")
    lines.append("Riferimento: ADR-001 (docs/adr/001-workflow-architecture.md).")
    return lines


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("DRIFT_CHECK_TOKEN")
    if not token:
        print("⚠️  Nessun token: API non autenticata (rate limit basso). "
              "Passa GITHUB_TOKEN/DRIFT_CHECK_TOKEN per risultati affidabili.")

    report = Report()
    for repo in REPOS:
        try:
            ref = default_branch(repo, token)
            workflows = fetch_workflows(repo, ref, token)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                print(f"[skip] {repo}: rate limit ({exc.code}) — riesegui con token")
                break
            raise
        if not workflows:
            continue
        check_test_audit(repo, workflows, report)
        check_inline_setup_python(repo, workflows, report)
        check_action_versions(repo, workflows, report)

    lines = render(report)
    print("\n".join(lines))
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as fh:
            fh.write("\n".join(["## Drift-check (ADR-001)", "", *lines, ""]))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
