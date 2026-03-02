from git_utils import get_staged_diff, commit_changes
from ai_core import generate_commit_message


def main():
    diff = get_staged_diff()

    if not diff:
        print("⚠ No staged changes found.")
        return

    print("🤖 Generating commit message...")
    message = generate_commit_message(diff)

    print("📝 Generated:", message)

    commit_changes(message)


if __name__ == "__main__":
    main()