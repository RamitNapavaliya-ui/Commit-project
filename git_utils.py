import subprocess
import sys


def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("❌ Git command failed:", e.stderr)
        sys.exit(1)


def get_staged_diff():
    return run_git_command(["git", "diff", "--cached"])


def get_current_branch():
    return run_git_command(["git", "branch", "--show-current"])


def commit_changes(message):
    if not message.strip():
        print("❌ Empty commit message.")
        sys.exit(1)

    run_git_command(["git", "commit", "-m", message])
    print("✅ Commit successful.")
    #testing the code for git commit