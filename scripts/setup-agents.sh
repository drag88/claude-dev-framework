#!/bin/bash

# CDF Setup Script
# Copies agents and scripts from plugin to ~/.claude/
# This ensures CDF components persist in the user's Claude folder after installation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "CDF Setup"
echo "========="
echo ""

# Determine plugin directory
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
    PLUGIN_DIR="$CLAUDE_PLUGIN_ROOT"
elif [ -d "$HOME/.claude/plugins/marketplaces/drag88/claude-dev-framework" ]; then
    PLUGIN_DIR="$HOME/.claude/plugins/marketplaces/drag88/claude-dev-framework"
else
    # Try to find it relative to this script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
fi

AGENTS_SOURCE="$PLUGIN_DIR/agents"
AGENTS_TARGET="$HOME/.claude/agents"
SCRIPTS_SOURCE="$PLUGIN_DIR/scripts"
SCRIPTS_TARGET="$HOME/.claude/scripts/cdf"

echo -e "${BLUE}Plugin directory:${NC} $PLUGIN_DIR"
echo ""

# ============================================
# SECTION 1: Setup Scripts (for user-level hooks)
# ============================================
echo -e "${BLUE}[1/2] Setting up scripts...${NC}"

# Create scripts directory
if [ ! -d "$SCRIPTS_TARGET" ]; then
    mkdir -p "$SCRIPTS_TARGET"
fi

SCRIPTS_CREATED=0
SCRIPTS_UPDATED=0

for script_file in "$SCRIPTS_SOURCE"/*.py "$SCRIPTS_SOURCE"/*.sh; do
    [ -e "$script_file" ] || continue
    filename=$(basename "$script_file")
    target_file="$SCRIPTS_TARGET/$filename"

    if [ -e "$target_file" ]; then
        if cmp -s "$script_file" "$target_file"; then
            : # Skip - identical
        else
            cp "$script_file" "$target_file"
            chmod +x "$target_file" 2>/dev/null || true
            echo -e "${YELLOW}Updated script:${NC} $filename"
            ((SCRIPTS_UPDATED++))
        fi
    else
        cp "$script_file" "$target_file"
        chmod +x "$target_file" 2>/dev/null || true
        echo -e "${GREEN}Created script:${NC} $filename"
        ((SCRIPTS_CREATED++))
    fi
done

if [ $SCRIPTS_CREATED -eq 0 ] && [ $SCRIPTS_UPDATED -eq 0 ]; then
    echo "  Scripts are up to date."
fi
echo ""

# ============================================
# SECTION 2: Setup Agents
# ============================================
echo -e "${BLUE}[2/2] Setting up agents...${NC}"

# Verify source directory exists
if [ ! -d "$AGENTS_SOURCE" ]; then
    echo -e "${RED}Error: Agents directory not found at $AGENTS_SOURCE${NC}"
    echo "Please ensure CDF is properly installed."
    exit 1
fi

# Create target directory if it doesn't exist
if [ ! -d "$AGENTS_TARGET" ]; then
    mkdir -p "$AGENTS_TARGET"
fi

# Count agents
AGENT_COUNT=$(find "$AGENTS_SOURCE" -name "*.md" -type f ! -name "README.md" | wc -l | tr -d ' ')
echo "Found $AGENT_COUNT agent files to install"
echo ""

# Copy agent files (not symlinks - actual copies)
CREATED=0
UPDATED=0
SKIPPED=0

for agent_file in "$AGENTS_SOURCE"/*.md; do
    filename=$(basename "$agent_file")

    # Skip README.md
    if [ "$filename" = "README.md" ]; then
        continue
    fi

    target_file="$AGENTS_TARGET/$filename"

    if [ -e "$target_file" ]; then
        # File exists - check if content is different
        if cmp -s "$agent_file" "$target_file"; then
            # Files are identical
            ((SKIPPED++))
        else
            # Files differ - update with new version
            cp "$agent_file" "$target_file"
            echo -e "${YELLOW}Updated:${NC} $filename"
            ((UPDATED++))
        fi
    else
        # File doesn't exist - create it
        cp "$agent_file" "$target_file"
        echo -e "${GREEN}Created:${NC} $filename"
        ((CREATED++))
    fi
done

# Also remove any old symlinks that might exist from previous versions
for target_file in "$AGENTS_TARGET"/*.md; do
    if [ -L "$target_file" ]; then
        filename=$(basename "$target_file")
        # Check if this symlink points to our plugin
        link_target=$(readlink "$target_file")
        if [[ "$link_target" == *"cdf/agents/"* ]]; then
            # Replace symlink with actual file
            rm "$target_file"
            if [ -f "$AGENTS_SOURCE/$filename" ]; then
                cp "$AGENTS_SOURCE/$filename" "$target_file"
                echo -e "${YELLOW}Converted symlink to file:${NC} $filename"
                ((UPDATED++))
            fi
        fi
    fi
done

echo ""
echo "======================================"
echo -e "${GREEN}CDF Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Summary:"
echo "  Scripts: $SCRIPTS_CREATED created, $SCRIPTS_UPDATED updated"
echo "  Agents:  $CREATED created, $UPDATED updated, $SKIPPED unchanged"
echo ""
echo "Installed to:"
echo -e "  ${BLUE}Scripts:${NC} $SCRIPTS_TARGET"
echo -e "  ${BLUE}Agents:${NC}  $AGENTS_TARGET"
echo ""
echo "You can now use CDF agents with @agent-name syntax:"
echo "  @backend-architect"
echo "  @system-architect"
echo "  @security-engineer"
echo "  etc."
echo ""
echo -e "${YELLOW}Note:${NC} Add hooks to ~/.claude/settings.json for PreToolUse/PostToolUse:"
echo "  python3 ~/.claude/scripts/cdf/keyword-amplifier.py"
echo "  python3 ~/.claude/scripts/cdf/comment-checker.py"
