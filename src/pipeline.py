from prefect import flow, task
from prefect.tasks import task_input_hash
import requests
import json
import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from pydantic_classes import Monster

@task(
    retries=3,
    retry_delay_seconds=10,
    log_prints=True,
    persist_result=True,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1)
)
def fetch_monster_list() -> List[Dict]:
    """Fetches the complete list of all available monsters from the D&D API.

    This tasks return is cached for one day.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains
                    a monster's name and its API URL endpoint.
                    Example: [{'index': 'aboleth', 'name': 'Aboleth', 'url': '/api/monsters/aboleth'}]
    """
    print("Fetching full monster list from API...")
    response = requests.get("https://www.dnd5eapi.co/api/monsters")
    response.raise_for_status()

    return response.json()["results"]

@task
def select_random_monsters(monster_list: List[Dict], count: int = 5) -> List[Dict]:
    """Selects a deterministic, random sample of monsters from the full list.

    The selection is idempotent for a given day. Running this task multiple
    times on the same day will yield the same list of monsters.

    Args:
        monster_list (List[Dict]): The full list of monsters from fetch_monster_list.
        count (int): The number of random monsters to select. Defaults to 5.

    Returns:
        List[Dict]: A new, smaller list containing the randomly selected monsters.
    """
    today_seed = datetime.now().strftime("%Y-%m-%d")
    seeded_random = random.Random(today_seed)
    selected_monsters = seeded_random.sample(monster_list, count)

    return selected_monsters

@task(
    retries=2,
    retry_delay_seconds=5,
    log_prints=True,
    persist_result=True,
    cache_key_fn=task_input_hash
)
def fetch_monster_details(monster_url: str) -> Dict:
    """Fetches detailed data for a single monster using its specific API URL.

    This task is cached indefinitely based on the monster's URL.

    Args:
        monster_url (str): The relative API endpoint for the monster
                           (e.g., '/api/monsters/goblin').

    Returns:
        Dict: A dictionary containing the full, raw details of the monster.

    Raises:
        requests.exceptions.HTTPError: If the API returns a non-200 status code.
    """
    try:
        base_url = "https://www.dnd5eapi.co"
        response = requests.get(f"{base_url}{monster_url}")
        response.raise_for_status()

        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error fetching {monster_url}: Status {e.response.status_code}")

        raise

@task(retries=2, retry_delay_seconds=5)
def transform_monster_data(raw_data: Dict) -> Dict:
    """Extracts a subset of fields from the raw monster data.

    Args:
        raw_data (Dict): The full dictionary of a monster's details.

    Returns:
        Dict: A new dictionary containing only the fields required for the output.
    """
    return {
        "name": raw_data["name"],
        "hit_points": raw_data["hit_points"],
        "armor_class": raw_data["armor_class"][0]["value"] if raw_data.get("armor_class") else None,
        "actions": [
            {"name": action["name"], "desc": action["desc"]}
            for action in raw_data.get("actions", [])
        ]
    }

@task
def validate_data(monster_data: Dict) -> Optional[Dict]:
    """Validates the transformed monster data against the Pydantic Monster schema.

    This task acts as a data quality gate. If the data does not conform to the
    `Monster` Pydantic model, the task will log the error and return None.

    Args:
        monster_data (Dict): A dictionary of transformed monster data.

    Returns:
        Optional[Dict]: The validated dictionary if it conforms to the schema,
                        otherwise None.
    """
    try:
        validated_monster = Monster(**monster_data)

        return validated_monster.model_dump()
    except Exception as e: # Catching a broad exception to be safe
        print(f"❌ Validation failed for monster: {monster_data.get('name', 'Unknown')}\n{e}")

        return None

@task
def write_output(monsters_data: List[Dict], output_path: str = "monsters.json"):
    """Writes the final list of validated monster data to a JSON file.

    Args:
        monsters_data (List[Dict]): The list of fully processed and validated
                                    monster dictionaries.
        output_path (str): The file path where the JSON output will be saved.
                           Defaults to "monsters.json".
    """
    with open(output_path, 'w') as f:
        json.dump(monsters_data, f, indent=4) # Changed indent to 4 for better readability
    print(f"✅ Successfully wrote {len(monsters_data)} monsters to {output_path}")

@flow(name="dnd-monster-pipeline")
def main_flow(num_monsters: int = 5):
    """The main ETL pipeline flow to fetch, process, and save monster data."""
    monster_list = fetch_monster_list()
    selected_monsters = select_random_monsters(monster_list, count=num_monsters)

    monster_urls = [monster["url"] for monster in selected_monsters]

    raw_data_results = fetch_monster_details.map(monster_urls)
    transformed_results = transform_monster_data.map(raw_data_results)
    validation_results = validate_data.map(transformed_results)

    # Filter out any monsters that failed validation (returned as None)
    final_monsters = [monster for monster in validation_results if monster is not None]

    write_output(final_monsters)