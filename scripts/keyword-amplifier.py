#!/usr/bin/env python3
"""
Keyword Amplifier Hook for Claude Code

PreToolUse hook that detects mode keywords in user messages and injects
contextual instructions to amplify Claude's behavior for specific tasks.

Keywords:
- "ultrawork" / "deep work" → Maximum focus mode with comprehensive analysis
- "search" / "find" → Thorough search with multiple strategies
- "analyze" / "analyse" → Structured analytical framework
- "think deeply" / "think hard" → Extended reasoning with multiple perspectives
- "investigate" → Root cause analysis mode
- "quick" / "fast" → Efficient execution with minimal overhead
"""

import json
import os
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

    "search": """
## ENHANCED SEARCH MODE

Apply multi-strategy search approach:

1. **Multiple Patterns**: Try variations (camelCase, snake_case, kebab-case)
2. **Semantic Search**: Look for synonyms and related concepts
3. **Structural Search**: Check likely locations based on project structure
4. **Cross-Reference**: Verify findings in multiple files
5. **Report All**: Include partial matches and near-misses""",

    "analyze": """
## STRUCTURED ANALYSIS MODE

Apply systematic analysis framework:

1. **Decomposition**: Break down into components
2. **Pattern Recognition**: Identify recurring patterns
3. **Dependency Mapping**: Trace relationships and dependencies
4. **Risk Assessment**: Identify potential issues
5. **Recommendation Synthesis**: Provide actionable insights

Present findings in structured format with evidence.""",

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

    "quick": """
## EFFICIENT EXECUTION MODE

Apply rapid execution principles:

1. **Direct Path**: Take the most straightforward approach
2. **Minimal Changes**: Only modify what's necessary
3. **Skip Elaboration**: Keep explanations concise
4. **Defer Optimization**: Good enough now, perfect later
5. **Fast Feedback**: Execute and iterate quickly"""
}

# Keyword patterns mapped to modes
KEYWORD_PATTERNS = [
    (r'\bultrawork\b', 'ultrawork'),
    (r'\bdeep\s*work\b', 'deep_work'),
    (r'\bthink\s*(deeply|hard|harder|carefully)\b', 'think_deeply'),
    (r'\b(search|find)\s*(for|through|across|in|the)?\b', 'search'),
    (r'\banalyze|analyse|analysis\b', 'analyze'),
    (r'\binvestigate\b', 'investigate'),
    (r'\b(quick|quickly|fast|rapid)\b', 'quick'),
]


def detect_mode(text: str) -> Optional[str]:
    """Detect which mode keyword is present in the text."""
    text_lower = text.lower()

    for pattern, mode in KEYWORD_PATTERNS:
        if re.search(pattern, text_lower):
            return mode

    return None


def main() -> None:
    """Main entry point for the hook."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No input or invalid JSON, exit silently
        print(json.dumps({}))
        return

    # Get the session transcript or last message
    session_messages = hook_input.get("session_messages", [])

    # Look for keywords in recent user messages (last 3)
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
            # Handle message with multiple content blocks
            for block in message:
                if isinstance(block, dict) and block.get("type") == "text":
                    detected_mode = detect_mode(block.get("text", ""))
                    if detected_mode:
                        break
            if detected_mode:
                break

    if detected_mode and detected_mode in AMPLIFICATION_MODES:
        result = {
            "additionalContext": AMPLIFICATION_MODES[detected_mode]
        }
    else:
        result = {}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
