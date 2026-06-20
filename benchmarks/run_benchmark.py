import asyncio
import json
import os
import sys
import datetime
sys.path.append(os.getcwd())
from core.brain import FridayBrain

async def run_benchmark():
    tasks_path = "benchmarks/tasks.json"
    if not os.path.exists(tasks_path):
        print("Tasks file not found.")
        return

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    brain = FridayBrain()
    results = []
    print(f"Friday: Commencing Benchmark Run ({len(tasks)} tasks)...")

    for t in tasks:
        print(f"Running Task {t['id']}: {t['task']}")
        transcript = ""
        passed = False
        try:
            # We call the real FridayBrain.chat_stream
            async for chunk in brain.chat_stream(t['task']):
                transcript += chunk

            # Heuristic for pass: either the system message or the presence of the tool name
            # We look for "Accessing [Tool]..." string which is emitted by our tool loop
            if f"Accessing {t['expected_tool']}..." in transcript:
                passed = True
            elif t['expected_tool'].lower() in transcript.lower():
                 # Slightly weaker check if system message was somehow missed but tool was discussed
                 passed = True
        except Exception as e:
            transcript = f"FAILED DURING EXECUTION: {e}"

        results.append({
            "id": t['id'],
            "task": t['task'],
            "passed": passed,
            "transcript_summary": transcript[:100].replace('\n', ' ') + "..."
        })

    # Save results
    pass_count = sum(1 for r in results if r['passed'])
    pass_rate = (pass_count / len(tasks)) * 100

    report = f"# FRIDAY BENCHMARK RESULTS - {datetime.date.today()}\n\n"
    report += f"**Overall Pass Rate:** {pass_rate}%\n\n"
    report += "| ID | Task | Status | Summary |\n"
    report += "|----|------|--------|---------|\n"
    for r in results:
        status = "✅ PASS" if r['passed'] else "❌ FAIL"
        report += f"| {r['id']} | {r['task']} | {status} | {r['transcript_summary']} |\n"

    with open("benchmarks/results.md", "w") as f:
        f.write(report)

    print(f"Benchmark complete. Pass Rate: {pass_rate}%. Results in benchmarks/results.md")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
