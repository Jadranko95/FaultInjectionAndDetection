import argparse
import cProfile
import pstats

from src.scenarios.race_condition_scenario import RaceConditionScenario
from src.scenarios.deadlock_scenario import DeadlockScenario
from src.scenarios.resource_contention_scenario import ResourceContentionScenario


def parse_args():
    parser = argparse.ArgumentParser(
        description="Concurrency Fault Injection Engine"
    )
    parser.add_argument(
        "scenario",
        choices=["race", "deadlock", "contention"],
        help="Scenario to run",
    )
    parser.add_argument(
        "--buggy",
        action="store_true",
        help="Enable buggy implementation (fault injected)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Thread count for race scenario",
    )
    parser.add_argument(
        "--increments",
        type=int,
        default=1000,
        help="Increments per thread for race scenario",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Timeout in seconds for deadlock watchdog",
    )
    parser.add_argument(
        "--variant",
        choices=["thread", "io", "cpu"],
        default="thread",
        help="Variant for resource contention scenario",
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable cProfile profiling for execution analysis",
    )
    return parser.parse_args()


def execute_scenario(args):
    if args.scenario == "race":
        scenario = RaceConditionScenario(
            threads_count=args.threads, increments_per_thread=args.increments
        )
        elapsed = scenario.run(buggy=args.buggy)
        print(
            f"Race Condition ({'buggy' if args.buggy else 'fixed'}): "
            f"Counter={scenario.counter}, Time={elapsed:.4f}s"
        )
    elif args.scenario == "deadlock":
        scenario = DeadlockScenario(timeout_seconds=args.timeout)
        elapsed = scenario.run(buggy=args.buggy)
        print(
            f"Deadlock ({'buggy' if args.buggy else 'fixed'}): Elapsed={elapsed:.4f}s"
        )
    elif args.scenario == "contention":
        scenario = ResourceContentionScenario(variant=args.variant)
        elapsed = scenario.run(buggy=args.buggy)
        print(
            f"Resource Contention [{args.variant}] ({'buggy' if args.buggy else 'fixed'}): "
            f"Elapsed={elapsed:.4f}s"
        )


def main():
    args = parse_args()

    if args.profile:
        print("🔍 Profiler enabled. Running execution under cProfile...\n")
        profiler = cProfile.Profile()
        profiler.enable()

        execute_scenario(args)

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumtime")
        print("\n--- PROFILER TOP 15 CUMULATIVE CALLS ---")
        stats.print_stats(15)
    else:
        execute_scenario(args)


if __name__ == "__main__":
    main()
