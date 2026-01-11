#!/usr/bin/env bash
# Test script for OpenCode patch installation

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "OpenCode Patch Installation Test"
echo "================================="
echo ""

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
test_condition() {
    local description="$1"
    local condition="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    echo -n "Testing: $description... "
    
    if eval "$condition"; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Run tests
echo "Pre-installation Checks"
echo "-----------------------"

test_condition "Patch directory exists" "[ -d '$REPO_ROOT/patch' ]"
test_condition "Installer script exists" "[ -f '$REPO_ROOT/patch/install-opencode-patch.sh' ]"
test_condition "Installer is executable" "[ -x '$REPO_ROOT/patch/install-opencode-patch.sh' ]"
test_condition "Commands directory exists" "[ -d '$REPO_ROOT/patch/commands/voice' ]"
test_condition "Wrappers directory exists" "[ -d '$REPO_ROOT/patch/wrappers' ]"

echo ""
echo "Command Definition Checks"
echo "-------------------------"

test_condition "converse.md exists" "[ -f '$REPO_ROOT/patch/commands/voice/converse.md' ]"
test_condition "install.md exists" "[ -f '$REPO_ROOT/patch/commands/voice/install.md' ]"
test_condition "status.md exists" "[ -f '$REPO_ROOT/patch/commands/voice/status.md' ]"
test_condition "help.md exists" "[ -f '$REPO_ROOT/patch/commands/voice/help.md' ]"
test_condition "config.md exists" "[ -f '$REPO_ROOT/patch/commands/voice/config.md' ]"

# Check command format
test_condition "converse.md has YAML frontmatter" "grep -q '^---$' '$REPO_ROOT/patch/commands/voice/converse.md'"
test_condition "converse.md has description" "grep -q '^description:' '$REPO_ROOT/patch/commands/voice/converse.md'"

echo ""
echo "Wrapper Script Checks"
echo "---------------------"

test_condition "voice-converse.py exists" "[ -f '$REPO_ROOT/patch/wrappers/voice-converse.py' ]"
test_condition "voice-status.py exists" "[ -f '$REPO_ROOT/patch/wrappers/voice-status.py' ]"
test_condition "voice-converse.py is executable" "[ -x '$REPO_ROOT/patch/wrappers/voice-converse.py' ]"
test_condition "voice-status.py is executable" "[ -x '$REPO_ROOT/patch/wrappers/voice-status.py' ]"
test_condition "voice-converse.py has shebang" "head -1 '$REPO_ROOT/patch/wrappers/voice-converse.py' | grep -q '#!/usr/bin/env python3'"
test_condition "voice-status.py has shebang" "head -1 '$REPO_ROOT/patch/wrappers/voice-status.py' | grep -q '#!/usr/bin/env python3'"

echo ""
echo "Documentation Checks"
echo "--------------------"

test_condition "OPENCODE_PATCH.md exists" "[ -f '$REPO_ROOT/OPENCODE_PATCH.md' ]"
test_condition "patch/README.md exists" "[ -f '$REPO_ROOT/patch/README.md' ]"
test_condition "OPENCODE_PATCH.md is not empty" "[ -s '$REPO_ROOT/OPENCODE_PATCH.md' ]"

echo ""
echo "Python Import Checks"
echo "--------------------"

if command -v python3 &> /dev/null; then
    test_condition "Python 3 available" "command -v python3 &> /dev/null"
    
    # Check if voice_mode is importable (might fail if not installed)
    if python3 -c "import voice_mode" 2>/dev/null; then
        test_condition "voice_mode package importable" "python3 -c 'import voice_mode'"
        test_condition "voice_mode.config importable" "python3 -c 'from voice_mode import config'"
        test_condition "voice_mode.core importable" "python3 -c 'from voice_mode import core'"
    else
        echo -e "${YELLOW}Note: voice_mode package not installed (expected if running from fresh checkout)${NC}"
    fi
else
    echo -e "${YELLOW}Python 3 not available - skipping import tests${NC}"
fi

echo ""
echo "Optional Dependency Checks"
echo "--------------------------"

test_condition "ffmpeg available" "command -v ffmpeg &> /dev/null" || echo -e "  ${YELLOW}Note: ffmpeg not installed (required for voice features)${NC}"
test_condition "uv available" "command -v uv &> /dev/null" || echo -e "  ${YELLOW}Note: uv not installed (recommended for installation)${NC}"
test_condition "opencode available" "command -v opencode &> /dev/null" || echo -e "  ${YELLOW}Note: opencode not installed (required for patch)${NC}"

echo ""
echo "Test Summary"
echo "============"
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "The patch is ready to install."
    echo "To install, run:"
    echo "  ./patch/install-opencode-patch.sh"
    exit 0
else
    echo -e "${RED}✗ Some tests failed.${NC}"
    echo ""
    echo "Please fix the issues above before installing the patch."
    exit 1
fi
