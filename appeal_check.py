#!/usr/bin/env python3
"""
Criterion 4: the appeal workflow, run three times.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python appeal_check.py --label before      # in another

run_eval.py only talks to /submit, so this file covers the appeal path. Each
trial:

  1. submits one of your evaluation texts and saves its content_id
  2. snapshots that submission's audit entries (exactly one, status "decided")
  3. POSTs a valid appeal
  4. checks the response, then re-reads the log and checks that
       - the original entry is untouched
       - one new entry was appended, with status "under_review"
       - the original entry still matches what /submit returned
  5. sends invalid appeals (unknown id, missing/empty/whitespace/non-string
   reasoning, missing id) and checks each gets a 4xx and creates a rejection
   entry rather than a normal decision or appeal entry

It writes results/appeal_<stamp>_<label>.md in the same style as run_eval.py.
It does not decide the verdict; read the checks and fill in the table.
"""

import argparse
import datetime as dt
import json
import sys

import config
import scenarios

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"
VALID_REASONING = "I wrote this myself and would like a person to review it."
DECISION_FIELDS = ("guess", "model_score", "style_score", "combined_score")

def unknown_id_for(trial):
    """Return a distinct unknown content ID for each trial."""
    return f"00000000-0000-0000-0000-{trial:012d}"

def safe_json(response):
    try:
        return response.json() if response.content else {}
    except ValueError:
        return {}


def entries_for(requests, url, content_id, timeout):
    """Every audit entry for one content_id, oldest first."""
    payload = safe_json(requests.get(f"{url}/log", timeout=timeout))
    return [e for e in payload.get("entries", []) if e.get("content_id") == content_id]


def run_trial(requests, url, trial, timeout):
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)})
        return bool(ok)

    # 1. A real decision to appeal.
    submit = requests.post(
        f"{url}/submit",
        json={"text": scenarios.HUMAN_SAMPLES[0], "creator_id": f"eval_appeal_{trial}"},
        timeout=timeout,
    )
    decision = safe_json(submit)
    if not check("submit returns 200", submit.status_code == 200, f"status {submit.status_code}"):
        return checks
    content_id = decision.get("content_id")
    if not check("submit returns a content_id", bool(content_id)):
        return checks

    # 2. Snapshot before the appeal.
    before = entries_for(requests, url, content_id, timeout)
    check("exactly one entry exists before the appeal", len(before) == 1, f"{len(before)} entries")
    check("that entry has status 'decided'",
          bool(before) and before[0].get("status") == "decided",
          before[0].get("status") if before else "no entry")

    # 3. A valid appeal.
    appeal = requests.post(
        f"{url}/appeal",
        json={"content_id": content_id, "reasoning": VALID_REASONING},
        timeout=timeout,
    )
    body = safe_json(appeal)
    check("valid appeal returns 200", appeal.status_code == 200, f"status {appeal.status_code}")
    check("appeal response reports status 'under_review'",
          body.get("status") == "under_review", body.get("status"))

    # 4. The log afterwards.
    after = entries_for(requests, url, content_id, timeout)
    check("exactly one entry was appended", len(after) == len(before) + 1,
          f"{len(before)} -> {len(after)}")
    check("original entry is unchanged", after[:len(before)] == before)
    appended = after[len(before):]
    check("appended entry has status 'under_review'",
          any(e.get("status") == "under_review" for e in appended),
          [e.get("status") for e in appended])
    if before:
        check("original entry matches what /submit returned",
              all(before[0].get(k) == decision.get(k) for k in DECISION_FIELDS),
              {k: (before[0].get(k), decision.get(k)) for k in DECISION_FIELDS})
    
    unknown_id = unknown_id_for(trial)

    # 5. Invalid appeals: rejected, and no new review record.
    invalid = [
        ("unknown content_id", {"content_id": unknown_id, "reasoning": VALID_REASONING}),
        ("missing content_id", {"reasoning": VALID_REASONING}),
        ("missing reasoning", {"content_id": content_id}),
        ("empty reasoning", {"content_id": content_id, "reasoning": ""}),
        ("whitespace-only reasoning", {"content_id": content_id, "reasoning": "   "}),
        ("non-string reasoning", {"content_id": content_id, "reasoning": 12345}),
    ]
    # Snapshot the original submission's entries before invalid appeals.
    before_invalid = entries_for(requests, url, content_id, timeout)

    for name, payload in invalid:
        r = requests.post(f"{url}/appeal", json=payload, timeout=timeout)
        check(f"invalid appeal rejected with 4xx: {name}",
              400 <= r.status_code < 500, f"status {r.status_code}")

    # Invalid requests linked to the original submission should create
    # rejection entries, not new decisions or appeals.
    after_invalid = entries_for(requests, url, content_id, timeout)
    new_entries = after_invalid[len(before_invalid):]

    check(
        "invalid appeals created only rejection entries",
        len(new_entries) == 4
        and all(
            e.get("event") == "rejected"
            and e.get("status") == "rejected"
            for e in new_entries
        ),
        f"{len(new_entries)} new entries: "
        f"{[e.get('event') for e in new_entries]}"
    )

    # The unknown ID should have one rejection record, not a decision
    # or an appeal record.
    unknown_entries = entries_for(requests, url, unknown_id, timeout)

    check(
        "unknown content_id created a rejection, not a decision",
        len(unknown_entries) == 1
        and unknown_entries[0].get("event") == "rejected"
        and unknown_entries[0].get("status") == "rejected"
        and unknown_entries[0].get("reason") == "appeal_submission_not_found",
        str(unknown_entries)
    )
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    all_trials = []
    for trial in range(1, args.trials + 1):
        try:
            checks = run_trial(requests, args.url, trial, args.timeout)
        except Exception as exc:  # noqa: BLE001
            checks = [{"check": "trial ran without an exception", "passed": False,
                       "detail": f"{type(exc).__name__}: {exc}"}]
        all_trials.append(checks)
        passed = sum(c["passed"] for c in checks)
        print(f"trial {trial}: {passed}/{len(checks)} checks passed")
        for c in checks:
            if not c["passed"]:
                print(f"    FAILED: {c['check']}  ({c['detail']})")

    write_report(all_trials, args)


def write_report(all_trials, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_{stamp}{label}.md"

    lines = [
        f"# Appeal check{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `appeal_check.py::main`",
        f"- Service: `app.py::appeal` · {len(all_trials)} trials · "
        f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Trial | Checks passed |",
        "|---|---|",
    ]
    for n, checks in enumerate(all_trials, 1):
        lines.append(f"| {n} | {sum(c['passed'] for c in checks)}/{len(checks)} |")
    lines += ["", "---", "", "## What actually came back", ""]
    for n, checks in enumerate(all_trials, 1):
        lines += [f"**Trial {n}**", "", "```json", json.dumps(checks, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()