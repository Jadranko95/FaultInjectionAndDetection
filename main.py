import argparse
from src.scenarios.deadlock_scenario import DeadlockScenario
from src.scenarios.race_condition_scenario import RaceConditionScenario


def run_race_condition(args: argparse.Namespace) -> None:
    print(f"\n[SCENARIO: Race Condition] (buggy={args.buggy})")
    scenario = RaceConditionScenario(
        threads_count=args.threads,
        increments_per_thread=args.increments,
    )
    expected = args.threads * args.increments
    actual = scenario.run(buggy=args.buggy)

    print(f"Expected count : {expected}")
    print(f"Actual count   : {actual}")
    print(f"Lost operations: {expected - actual}")

    if args.buggy and actual < expected:
        print("RESULT: Race condition detected successfully (data corruption confirmed).")
    elif not args.buggy and actual == expected:
        print("RESULT: Synchronized execution completed deterministically.")
    else:
        print("RESULT: Unexpected result outcome.")


def run_deadlock(args: argparse.Namespace) -> None:
    print(f"\n[SCENARIO: Deadlock] (buggy={args.buggy})")
    scenario = DeadlockScenario(timeout_seconds=args.timeout)
    success = scenario.run(buggy=args.buggy)

    if not success:
        print(f"RESULT: Deadlock triggered! Threads hung for >{args.timeout}s.")
    else:
        print("RESULT: Transfers completed successfully with ordered locking.")
        print(
            f"Balances -> Account A: {scenario.acc_a.balance}, Account B: {scenario.acc_b.balance}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI Runner for Concurrency Fault Injection and Detection Scenarios."
    )
    subparsers = parser.add_subparsers(
        dest="scenario", required=True, help="Target fault scenario"
    )

    # Subparser: Race Condition
    race_parser = subparsers.add_parser("race", help="Execute Race Condition scenario")
    race_parser.add_argument(
        "--buggy", action="store_true", help="Run buggy (unlocked) implementation"
    )
    race_parser.add_argument(
        "--threads", type=int, default=10, help="Number of threads (default: 10)"
    )
    race_parser.add_argument(
        "--increments", type=int, default=1000, help="Increments per thread (default: 1000)"
    )
    race_parser.set_defaults(func=run_race_condition)

    # Subparser: Deadlock
    deadlock_parser = subparsers.add_parser("deadlock", help="Execute Deadlock scenario")
    deadlock_parser.add_argument(
        "--buggy", action="store_true", help="Run buggy (out-of-order locks) implementation"
    )
    deadlock_parser.add_argument(
        "--timeout", type=float, default=1.0, help="Safety timeout in seconds (default: 1.0)"
    )
    deadlock_parser.set_defaults(func=run_deadlock)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
