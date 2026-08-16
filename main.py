import argparse
from src.scenarios.deadlock_scenario import DeadlockScenario
from src.scenarios.race_condition_scenario import RaceConditionScenario
from src.scenarios.resource_contention_scenario import ResourceContentionScenario


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


def run_deadlock(args: argparse.Namespace) -> None:
    print(f"\n[SCENARIO: Deadlock] (buggy={args.buggy})")
    scenario = DeadlockScenario(timeout_seconds=args.timeout)
    success = scenario.run(buggy=args.buggy)

    if not success:
        print(f"RESULT: Deadlock triggered! Threads hung for >{args.timeout}s.")
    else:
        print("RESULT: Transfers completed successfully with ordered locking.")


def run_resource_contention(args: argparse.Namespace) -> None:
    print(
        f"\n[SCENARIO: Resource Contention - {args.variant.upper()}] (buggy={args.buggy})"
    )
    scenario = ResourceContentionScenario(variant=args.variant)
    elapsed = scenario.run(buggy=args.buggy)

    print(f"Variant      : {args.variant}")
    print(f"Elapsed time : {elapsed:.4f} seconds")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI Runner for Concurrency Fault Scenarios."
    )
    subparsers = parser.add_subparsers(
        dest="scenario", required=True, help="Target fault scenario"
    )

    # Race Condition
    race_parser = subparsers.add_parser("race", help="Race Condition scenario")
    race_parser.add_argument("--buggy", action="store_true")
    race_parser.add_argument("--threads", type=int, default=10)
    race_parser.add_argument("--increments", type=int, default=1000)
    race_parser.set_defaults(func=run_race_condition)

    # Deadlock
    deadlock_parser = subparsers.add_parser("deadlock", help="Deadlock scenario")
    deadlock_parser.add_argument("--buggy", action="store_true")
    deadlock_parser.add_argument("--timeout", type=float, default=1.0)
    deadlock_parser.set_defaults(func=run_deadlock)

    # Resource Contention
    contention_parser = subparsers.add_parser(
        "contention", help="Resource Contention scenario"
    )
    contention_parser.add_argument("--buggy", action="store_true")
    contention_parser.add_argument(
        "--variant",
        choices=["thread", "io", "cpu"],
        default="thread",
        help="Target contention variant (thread | io | cpu)",
    )
    contention_parser.set_defaults(func=run_resource_contention)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
