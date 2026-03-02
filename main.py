import argparse
import sys
from git_utils import get_staged_diff, commit_changes
from ai_core import generate_commit, generate_branch, generate_pr


def main():
    parser = argparse.ArgumentParser(description="AI Git Assistant")

    parser.add_argument("command", choices=["commit", "branch", "pr"])
    parser.add_argument("--auto", action="store_true", help="Auto commit without confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Generate but do not execute")

    args = parser.parse_args()

    print("🔍 Checking staged changes...")
    diff = get_staged_diff()

    if not diff.strip():
        print("⚠ No staged changes found. Use 'git add .' first.")
        sys.exit(1)

    if args.command == "commit":
        msg = generate_commit(diff)

        if "API Error" in msg:
            print(msg)
            sys.exit(1)

        print("\n📝 Suggested Commit:\n")
        print(msg)

        if args.dry_run:
            print("\n(Dry run mode - commit not executed)")
            return

        if args.auto:
            commit_changes(msg)
        else:
            confirm = input("\nCommit with this message? (y/n): ")
            if confirm.lower() == "y":
                commit_changes(msg)
            else:
                print("❌ Commit cancelled.")

    elif args.command == "branch":
        branch = generate_branch(diff)
        print("\n🌿 Suggested Branch Name:\n")
        print(branch)

    elif args.command == "pr":
        pr_desc = generate_pr(diff)
        print("\n📄 Generated PR Description:\n")
        print(pr_desc)


if __name__ == "__main__":
    main()


