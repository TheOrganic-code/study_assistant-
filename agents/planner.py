import datetime
import json
import os


def make_plan(topics, start_date=None, gap_days=2, include_revision=True, skip_weekends=True):
    """
    Generate a smart study plan using spaced repetition principles.

    Args:
        topics (list): List of topics to study.
        start_date (datetime.date, optional): When to start the plan.
        gap_days (int): Days between each new topic.
        include_revision (bool): Add automatic review sessions.
        skip_weekends (bool): Skip scheduling on weekends.

    Returns:
        list: Structured list of {topic, study_date, review_date}
    """
    if not topics:
        raise ValueError("No topics provided for planning!")

    today = start_date or datetime.date.today()
    plan = []
    current_date = today

    for i, topic in enumerate(topics):
        # --- Calculate study date ---
        if i > 0:
            current_date += datetime.timedelta(days=gap_days)

        # Skip weekends if necessary
        while skip_weekends and current_date.weekday() >= 5:  # 5=Sat,6=Sun
            current_date += datetime.timedelta(days=1)

        entry = {
            "topic": topic,
            "study_on": current_date.strftime("%A, %d %B %Y"),
        }

        # --- Add spaced review sessions ---
        if include_revision:
            review_1 = current_date + datetime.timedelta(days=2)
            review_2 = current_date + datetime.timedelta(days=5)

            if skip_weekends and review_1.weekday() >= 5:
                review_1 += datetime.timedelta(days=(7 - review_1.weekday()))
            if skip_weekends and review_2.weekday() >= 5:
                review_2 += datetime.timedelta(days=(7 - review_2.weekday()))

            entry["reviews"] = [
                review_1.strftime("%A, %d %B %Y"),
                review_2.strftime("%A, %d %B %Y"),
            ]

        plan.append(entry)

    # --- Save JSON ---
    os.makedirs("outputs", exist_ok=True)
    file_path = os.path.join("outputs", "planner.json")
    with open(file_path, "w") as f:
        json.dump(plan, f, indent=2)

    return plan


# Example usage:
if __name__ == "__main__":
    example_topics = ["Neural Networks", "Data Preprocessing", "CNNs", "Transformers", "Model Evaluation"]
    study_plan = make_plan(example_topics)
    for p in study_plan:
        print(f"📘 {p['topic']} → Study on {p['study_on']}")
        if "reviews" in p:
            print(f"   🔁 Review on {', '.join(p['reviews'])}")

