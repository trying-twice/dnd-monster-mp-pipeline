# dnd-monster-pipeline
Pipeline challenge for MediaProbe Internship.
---

# 🐉 Dungeons & Data: Monster Pipeline

This project is a simple, orchestrated data pipeline built with Prefect and Docker. It fetches monster data from the D&D 5e API, cleans it, and saves the result as a JSON file.

## What it Does
*   Fetches a list of monsters from the [D&D 5e API](https://www.dnd5eapi.co/).
*   Selects a random, deterministic sample of monsters for the day.
*   Transforms and validates the data using Pydantic for a clean schema.
*   Saves the final, clean data to `monsters.json`.

## Technology Used
*   **Python**
*   **Prefect**: For pipeline orchestration.
*   **Docker** & **Docker Compose**: For containerization and running services.
*   **Pydantic**: For data validation.

## Requirements
- Limit fetched results via API filters or pagination ✅   
(The pipeline first fetches the full list of monster names, then selects a small, configurable number of them (e.g., 5) before fetching their heavy, detailed data. This limits the main API load to only the monsters we need.)
- Make pipeline idempotent (don’t re-fetch if file exists) ✅   
(Monster selection is seeded with the current date, guaranteeing the same "random" monsters are chosen for any run on the same day. This makes the pipeline's output reproducible.)
- Add CLI arguments for monster selection ✅   
(The main.py entrypoint uses Python's standard argparse library to accept a --num-monsters command-line argument, which is then passed as a parameter to the main Prefect flow.)
- Cache API response locally ✅   
(The Prefect @task decorator is configured with persist_result=True and cache_key_fn=task_input_hash on API-calling functions. This automatically saves a task's output and reuses it on subsequent runs with the same inputs, preventing re-fetching.)
- Add unit tests for task components ❌   
( Unit tests would be added using a framework like pytest to validate the logic of individual tasks (especially transformation and validation) by providing mock inputs and asserting their outputs.)

---

## How to Run

### Prerequisites
*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/dnd-monster-pipeline.git
cd dnd-monster-pipeline
```

### 2. Start the Services
This command starts the Prefect server and database in the background.
```bash
docker compose up -d
```
You can view the Prefect dashboard at [http://localhost:4200](http://localhost:4200).

### 3. Run the Pipeline
Execute the pipeline inside the running container.

**To run with the default of 5 monsters:**
```bash
docker compose exec prefect-server python src/main.py
```

**To specify a different number of monsters:**
```bash
docker compose exec prefect-server python src/main.py --num-monsters 15
```

---

## Output
After the pipeline runs, you will find a **`monsters.json`** file in your project directory containing the final data.

## Shutting Down
To stop and remove the containers, run:
```bash
docker compose down
```

## Note for Linux Users: Handling the `sudo` Requirement

On new Linux systems (including VMs and WSL), you may find that you need to run all `docker` commands with `sudo`. This is a standard permissions issue that should be fixed with a one-time setup to avoid security risks and file ownership problems.

### One-Time Setup Instructions

Follow these steps to add your user to the `docker` group, which is the official and recommended way to manage Docker permissions.

**1. Add your user to the `docker` group.**
*(The group may already exist, which is fine.)*
## This command creates the 'docker' group if it doesn't exist

```bash
sudo groupadd docker
```

## This command adds your current user to the 'docker' group
sudo usermod -aG docker $USER

2. IMPORTANT: Apply the new group membership.
For the changes to take effect, you must either log out and log back in or completely reboot your system.

3. Verify the fix.
After logging back in, open a new terminal and test that you can run Docker commands without sudo.
code.
    
## This command should now run without asking for a password
docker ps

  