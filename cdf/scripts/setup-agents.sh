#!/bin/bash

# CDF Agent Setup Script
# Creates symlinks from plugin agents to ~/.claude/agents/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "CDF Agent Setup"
echo "==============="
echo ""

# Determine plugin directory
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
    PLUGIN_DIR="$CLAUDE_PLUGIN_ROOT"
elif [ -d "$HOME/.claude/plugins/marketplaces/aswin-plugins/cdf" ]; then
    PLUGIN_DIR="$HOME/.claude/plugins/marketplaces/aswin-plugins/cdf"
else
    # Try to find it relative to this script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
fi

AGENTS_SOURCE="$PLUGIN_DIR/agents"
AGENTS_TARGET="$HOME/.claude/agents"

# Verify source directory exists
if [ ! -d "$AGENTS_SOURCE" ]; then
    echo -e "${RED}Error: Agents directory not found at $AGENTS_SOURCE${NC}"
    echo "Please ensure CDF is properly installed."
    exit 1
fi

# Create target directory if it doesn't exist
if [ ! -d "$AGENTS_TARGET" ]; then
    echo "Creating $AGENTS_TARGET..."
    mkdir -p "$AGENTS_TARGET"
fi

# Count agents
AGENT_COUNT=$(find "$AGENTS_SOURCE" -name "*.md" -type f ! -name "README.md" | wc -l | tr -d ' ')
echo "Found $AGENT_COUNT agent files in $AGENTS_SOURCE"
echo ""

# Create symlinks
CREATED=0
UPDATED=0
SKIPPED=0

for agent_file in "$AGENTS_SOURCE"/*.md; do
    filename=$(basename "$agent_file")

    # Skip README.md
    if [ "$filename" = "README.md" ]; then
        continue
    fi

    target_link="$AGENTS_TARGET/$filename"

    if [ -L "$target_link" ]; then
        # Symlink exists - check if it points to the right place
        current_target=$(readlink "$target_link")
        if [ "$current_target" = "$agent_file" ]; then
            ((SKIPPED++))
        else
            # Update symlink
            rm "$target_link"
            ln -s "$agent_file" "$target_link"
            echo -e "${YELLOW}Updated:${NC} $filename"
            ((UPDATED++))
        fi
    elif [ -e "$target_link" ]; then
        # File exists but is not a symlink - don't overwrite
        echo -e "${YELLOW}Skipped:${NC} $filename (file already exists, not a symlink)"
        ((SKIPPED++))
    else
        # Create new symlink
        ln -s "$agent_file" "$target_link"
        echo -e "${GREEN}Created:${NC} $filename"
        ((CREATED++))
    fi
done

echo ""
echo "Summary:"
echo "  Created: $CREATED"
echo "  Updated: $UPDATED"
echo "  Skipped: $SKIPPED"
echo ""

if [ $CREATED -gt 0 ] || [ $UPDATED -gt 0 ]; then
    echo -e "${GREEN}Setup complete!${NC}"
    echo ""
    echo "You can now use CDF agents with @agent-name syntax:"
    echo "  @backend-architect"
    echo "  @system-architect"
    echo "  @security-engineer"
    echo "  etc."
else
    echo "No changes made. Agents are already set up."
fi
