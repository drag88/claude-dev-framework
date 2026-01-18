# Failure Recovery Skill

Protocol for handling consecutive failures to prevent thrashing and wasted effort.

## When to Activate

- Same operation fails 3 times consecutively
- Different approaches to the same problem all fail
- Test suite keeps failing after multiple fix attempts
- Build errors persist after several corrections
- Search queries return no useful results repeatedly

## Three-Failure Protocol

After 3 consecutive failures on the same objective:

```
STOP → REVERT → DOCUMENT → CONSULT
```

### 1. STOP

Immediately halt the current approach. Do not:
- Try "one more variation"
- Make additional speculative changes
- Continue down the failing path

### 2. REVERT

Restore to last known good state:

```bash
# If changes were made to files
git checkout -- <affected-files>

# If in middle of complex operation
git stash

# If commits were made
git reset --soft HEAD~N  # where N = number of bad commits
```

### 3. DOCUMENT

Create a failure record:

```markdown
## Failure Record: [Brief Description]

**Objective**: What was being attempted

**Attempts**:
1. [First approach] → [Why it failed]
2. [Second approach] → [Why it failed]
3. [Third approach] → [Why it failed]

**Observations**:
- [Pattern noticed across failures]
- [Unexpected behavior]
- [Missing information]

**Hypotheses**:
- [What might actually be wrong]
- [What assumptions might be incorrect]
```

### 4. CONSULT

Ask the user for guidance:

```
I've attempted this 3 times without success:

**Goal**: [What I was trying to do]

**Approaches tried**:
1. [Approach 1]: [Result]
2. [Approach 2]: [Result]
3. [Approach 3]: [Result]

**What I think might be happening**:
[Hypothesis]

**Options**:
1. [Alternative approach A]
2. [Alternative approach B]
3. [Ask for more context about X]

Which would you like me to try, or do you have other suggestions?
```

## Failure Categories

### Build/Compile Failures
- Check for missing dependencies
- Verify environment setup
- Look for version mismatches
- Check import paths

### Test Failures
- Isolate the failing test
- Check test assumptions
- Verify test data setup
- Look for timing/async issues

### Search Failures
- Broaden search terms
- Check for typos in patterns
- Try different file patterns
- Consider renamed/moved files

### Edit Failures
- Verify file exists and path is correct
- Check for conflicting changes
- Ensure proper encoding
- Look for merge conflicts

### Runtime Failures
- Check logs for stack traces
- Verify environment variables
- Look for missing configurations
- Check network/service dependencies

## Recovery Strategies

### Incremental Rollback
```
1. Identify last known working state
2. Roll back to that state
3. Apply changes one at a time
4. Test after each change
5. Stop at first failure
```

### Minimal Reproduction
```
1. Create smallest possible failing case
2. Remove all unrelated code
3. Test the minimal case
4. Identify the specific trigger
```

### Divide and Conquer
```
1. Split the problem in half
2. Test each half independently
3. Focus on the failing half
4. Repeat until isolated
```

### Fresh Start
```
1. Abandon current changes completely
2. Return to clean state
3. Plan new approach from scratch
4. Document what NOT to do
```

## Prevention Practices

- **Commit early, commit often**: Small commits make rollback easier
- **Test incrementally**: Verify each change before proceeding
- **Read before writing**: Understand the code before modifying
- **One thing at a time**: Don't mix multiple changes

## Related Skills

- `external-memory` - Document failures in notes.md
- `context-saver` - Save progress before risky operations
