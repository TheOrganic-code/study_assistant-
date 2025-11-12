import datetime
import json
import os

def make_plan(topics, gap_days=2, output_path="outputs/planner.json"):
    """
    Create a smart revision plan for the given topics.
    
    Each topic is scheduled 'gap_days' apart from today.
    Example: if gap_days=2, the 1st topic is in 2 days, the next in 4, etc.
    """
    today = datetime.date.today()
    plan = []

    for i, topic in enumerate(topics):
        plan.append({
            "topic": topic,
            "revise_on": (today + datetime.timedelta(days=(i + 1) * gap_days)).strftime("%Y-%m-%d")
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(plan, f, indent=2)

    return plan
