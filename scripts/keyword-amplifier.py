#!/usr/bin/env python3
"""
Keyword Amplifier Hook for Claude Code

PreToolUse hook that detects mode keywords in user messages and injects
contextual instructions to amplify Claude's behavior for specific tasks.

Keywords:
- "ultrawork" / "deep work" → Maximum focus mode with comprehensive analysis
- "think deeply" / "think hard" → Extended reasoning with multiple perspectives
- "investigate" → Root cause analysis mode (standalone at start of message)
- "normal" / "reset" → Deactivate any injected mode
"""

import json
import sys
import re
from typing import Optional

# Mode amplification instructions
AMPLIFICATION_MODES = {
    "ultrawork": """
## ULTRAWORK MODE ACTIVATED

You are now in maximum focus mode. Apply these principles:

1. **Comprehensive Analysis**: Examine every aspect of the problem before acting
2. **Quality Over Speed**: Take time to produce excellent results
3. **Thorough Documentation**: Document decisions and reasoning
4. **No Shortcuts**: Complete all steps fully, no approximations
5. **Verification**: Double-check all outputs before presenting

Work systematically through the task with full attention to detail.""",

    "deep_work": """
## DEEP WORK MODE ACTIVATED

Enter a state of focused concentration:

1. **Single-Task Focus**: Complete one task fully before moving to the next
2. **Minimize Context Switching**: Group related operations
3. **Deep Understanding**: Read and understand before modifying
4. **Careful Execution**: Measure twice, cut once
5. **Complete Deliverables**: Finish what you start""",

    "think_deeply": """
## EXTENDED REASONING MODE

Apply deep thinking protocol:

1. **Multiple Perspectives**: Consider from different angles
2. **Challenge Assumptions**: Question what seems obvious
3. **Explore Alternatives**: Generate multiple solutions before choosing
4. **Consider Consequences**: Think through implications
5. **Synthesis**: Integrate insights into coherent conclusion

Take time to reason thoroughly before acting.""",

    "investigate": """
## INVESTIGATION MODE

Apply root cause analysis protocol:

1. **Symptom Documentation**: Record what you observe
2. **Hypothesis Generation**: Form multiple theories
3. **Evidence Gathering**: Collect data to test hypotheses
4. **Elimination**: Rule out possibilities systematically
5. **Root Cause Identification**: Trace to the source

Document the investigation trail for future reference.""",

    "normal": ""
}

# Keyword patterns mapped to modes (compiled once at import time)
# "normal"/"reset" checked first to allow deactivation
KEYWORD_PATTERNS = [
    (re.compile(r'\b(normal\s+mode|reset\s+mode)\b'), 'normal'),
    (re.compile(r'\bultrawork\b'), 'ultrawork'),
    (re.compile(r'\bdeep\s*work\b'), 'deep_work'),
    (re.compile(r'\bthink\s*(deeply|hard|harder|carefully)\b'), 'think_deeply'),
    (re.compile(r'^\s*investigate\b'), 'investigate'),
]

# Fast pre-filter: if none of these substrings appear, skip regex entirely
_FAST_KEYWORDS = frozenset([
    'ultrawork', 'deep', 'work', 'think', 'investigate',
    'normal', 'reset',
])


def _has_potential_keyword(text_lower: str) -> bool:
    """Fast substring check before expensive regex matching."""
    words = text_lower.split()
    return bool(_FAST_KEYWORDS.intersection(words))


def detect_mode(text: str) -> Optional[str]:
    """Detect which mode keyword is present in the text."""
    text_lower = text.lower()

    # Fast exit: no potential keywords found via substring check
    if not _has_potential_keyword(text_lower):
        return None

    for pattern, mode in KEYWORD_PATTERNS:
        if pattern.search(text_lower):
            return mode

    return None


def _extract_user_text(hook_input: dict) -> str:
    """Extract all recent user message text as a single lowercase string for fast keyword check."""
    session_messages = hook_input.get("session_messages", [])
    parts = []
    for msg in session_messages[-5:]:
        if msg.get("role") != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
    return " ".join(parts)


def main() -> None:
    """Main entry point for the hook."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    # Early exit: check if any keywords exist in user messages before doing anything else
    combined_text = _extract_user_text(hook_input)
    if not combined_text or not _has_potential_keyword(combined_text.lower()):
        return

    # Keywords detected - find which mode matches (check most recent message first)
    session_messages = hook_input.get("session_messages", [])
    user_messages = [
        msg.get("content", "")
        for msg in session_messages[-5:]
        if msg.get("role") == "user"
    ]

    detected_mode = None
    for message in reversed(user_messages):
        if isinstance(message, str):
            detected_mode = detect_mode(message)
            if detected_mode:
                break
        elif isinstance(message, list):
            for block in message:
                if isinstance(block, dict) and block.get("type") == "text":
                    detected_mode = detect_mode(block.get("text", ""))
                    if detected_mode:
                        break
            if detected_mode:
                break

    if detected_mode and detected_mode in AMPLIFICATION_MODES:
        context = AMPLIFICATION_MODES[detected_mode]
        if context:
            print(json.dumps({"additionalContext": context}))
        # "normal" mode: empty string means no context injected (deactivation)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        from pathlib import Path
        from datetime import datetime
        log_dir = Path.home() / '.cdf-logs'
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / 'hook-errors.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} [keyword-amplifier.py] {e}\n")
