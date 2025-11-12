import datetime
import json

def make_plan(topics):
    today = datetime.date.today()
    plan = []
    for i, topic in enumerate(topics):
        plan.append({
            "topic": topic,
            "revise_on": str(today + datetime.timedelta(days=(i+1)*2))
        })
    with open("outputs/planner.json", "w") as f:
        json.dump(plan, f, indent=2)
    return plan
