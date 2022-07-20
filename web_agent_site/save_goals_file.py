import json
import random
from web_agent_site.engine.engine import (
    load_products,
    init_search_engine,
)
from web_agent_site.engine.goal import get_goals
from web_agent_site.utils import (
    DEFAULT_FILE_PATH,
    DEBUG_PROD_SIZE,
)


if __name__ == "__main__":
    all_products, product_item_dict, product_prices, attribute_to_asins = \
        load_products(
            filepath=DEFAULT_FILE_PATH,
            num_products=DEBUG_PROD_SIZE
        )
    search_engine = init_search_engine(num_products=DEBUG_PROD_SIZE)
    goals = get_goals(all_products, product_prices)

    goals = [{"uuid": g["uuid"], "instruction_text": g["instruction_text"]} for g in goals]

    goal_uuid_to_goal = {}
    for goal in goals:
        if goal["uuid"] in goal_uuid_to_goal and goal["instruction_text"] != goal_uuid_to_goal[goal["uuid"]]["instruction_text"]:
            print("Found collision")
            print(f"{goal['instruction_text']}")
            print(f"{goal_uuid_to_goal[goal['uuid']]['instruction_text']}")
        else:
            goal_uuid_to_goal[goal["uuid"]] = goal

    # Remove duplicates based on uuid
    goal_uuid_to_goal = {goal["uuid"]: goal for goal in goals}
    print(f"Found {len(goals) - len(goal_uuid_to_goal)} / {len(goals)} duplicates. Total {len(goal_uuid_to_goal)} goals")
    goals = list(goal_uuid_to_goal.values())

    # Split goals into train, dev, and test splits
    random.seed(233)
    random.shuffle(goals)
    num_train_goals = 10_400
    num_dev_goals = 1000
    train_goals = goals[:num_train_goals]
    dev_goals = goals[num_train_goals:num_train_goals + num_dev_goals]
    test_goals = goals[num_train_goals + num_dev_goals:]
    print(f"Found {len(goals)} goals")
    print(f"Found {len(train_goals)} train goals")
    print(f"Found {len(dev_goals)} dev goals")
    print(f"Found {len(test_goals)} test goals")

    # Save to json
    with open("goals.json", "w") as f:
        json.dump(goals, f)
    with open("train_goals.json", "w") as f:
        json.dump(train_goals, f)
    with open("dev_goals.json", "w") as f:
        json.dump(dev_goals, f)
    with open("test_goals.json", "w") as f:
        json.dump(test_goals, f)
