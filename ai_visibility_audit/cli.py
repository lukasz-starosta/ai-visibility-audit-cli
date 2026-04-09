from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Sequence

from .api_client import request_live_scan, resolve_api_config
from .checks import CHECKS_VERSION, list_checks, render_check_catalog
from .inputs import AuditRequest
from .reports import build_artifacts


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-visibility-audit",
        description="Run AI Visibility Audit by PromptScout and write shareable artifacts.",
    )
    parser.add_argument("--domain")
    parser.add_argument("--page-limit", type=int, default=10)
    parser.add_argument("--citation-url", action="append", default=[])
    parser.add_argument("--pinned-url", action="append", default=[])
    parser.add_argument("--input-file")
    parser.add_argument("--response-file")
    parser.add_argument("--output-dir")
    parser.add_argument("--api-url")
    parser.add_argument("--api-key")
    parser.add_argument("--brand-id")
    parser.add_argument("--request-timeout-seconds", type=float, default=30.0)
    parser.add_argument("--show-checks", action="store_true")
    parser.add_argument(
        "--stdout-format",
        choices=["summary", "markdown", "json"],
        default="summary",
    )
    return parser


def _load_request(args: argparse.Namespace) -> AuditRequest:
    if args.input_file:
        return AuditRequest.model_validate_json(Path(args.input_file).read_text())

    if not args.domain:
        raise ValueError("Either --domain or --input-file is required.")

    return AuditRequest(
        domain=args.domain,
        page_limit=args.page_limit,
        citation_urls=args.citation_url,
        pinned_urls=args.pinned_url,
    )


def _load_response_file(path_value: str) -> dict:
    return json.loads(Path(path_value).read_text())


def _write_outputs(output_dir: str, artifacts) -> list[Path]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    json_path = destination / "ai-visibility-audit.json"
    markdown_path = destination / "ai-visibility-audit.md"
    summary_path = destination / "ai-visibility-audit.txt"

    json_path.write_text(json.dumps(artifacts.structured, indent=2) + "\n")
    markdown_path.write_text(artifacts.markdown + "\n")
    summary_path.write_text(artifacts.summary + "\n")

    return [json_path, markdown_path, summary_path]


async def _run(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)

    if args.show_checks:
        if args.stdout_format == "json":
            print(
                json.dumps(
                    {
                        "checksVersion": CHECKS_VERSION,
                        "checks": list_checks(),
                    },
                    indent=2,
                )
            )
        else:
            print(render_check_catalog())
        return 0

    request = _load_request(args)

    if args.response_file:
        scan_response = _load_response_file(args.response_file)
    else:
        config = resolve_api_config(
            api_url=args.api_url,
            api_key=args.api_key,
            brand_id=args.brand_id,
            timeout_seconds=args.request_timeout_seconds,
        )
        scan_response = await request_live_scan(request, config)

    artifacts = build_artifacts(request, scan_response)

    if args.output_dir:
        written_paths = _write_outputs(args.output_dir, artifacts)
        print("\n".join(str(path) for path in written_paths))
        return 0

    if args.stdout_format == "json":
        print(json.dumps(artifacts.structured, indent=2))
        return 0
    if args.stdout_format == "markdown":
        print(artifacts.markdown)
        return 0

    print(artifacts.summary)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    return asyncio.run(_run(argv))


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
