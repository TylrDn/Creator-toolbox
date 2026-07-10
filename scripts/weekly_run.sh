#!/usr/bin/env python3
"""Run the orchestrator for a content calendar week (human-in-the-loop drafts).

Usage:
    ./scripts/weekly_run.sh 3
    ./scripts/weekly_run.sh 3 --workflow product_launch --var product_name="Custom Jobs"
"""

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WEEK="${1:-1}"
shift || true

WORKFLOW=""
EXTRA_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workflow) WORKFLOW="$2"; shift 2 ;;
    *) EXTRA_ARGS+=("$1"); shift ;;
  esac
done

if [[ -z "$WORKFLOW" ]]; then
  case "$WEEK" in
    1|4|11) WORKFLOW="gta6_news_drop" ;;
    3|9)    WORKFLOW="product_launch" ;;
    6|10)   WORKFLOW="rp_server_launch" ;;
    7)      WORKFLOW="npc_pack_release" ;;
    *)      WORKFLOW="gta6_news_drop" ;;
  esac
fi

TOPIC=$(python3 - <<PY
import yaml
from pathlib import Path
data = yaml.safe_load(Path("content/calendar.yaml").read_text())
weeks = data.get("weeks", [])
week = next((w for w in weeks if w.get("week") == $WEEK), None)
print(week.get("topic", "Creator update") if week else "Creator update")
PY
)

echo "Week $WEEK -> workflow: $WORKFLOW"
echo "Topic: $TOPIC"

python3 -m orchestrator "$WORKFLOW" \
  --var "summary=$TOPIC" \
  --var "hook=$TOPIC" \
  --var "news_type=update" \
  --var "source=https://www.rockstargames.com/newswire" \
  --var "cta=Join Discord" \
  --out --log \
  "${EXTRA_ARGS[@]}"

echo "Draft saved under output/ — edit before publishing."
