# 🐉 Dungeons & Data: A Prefect Monster Pipeline

This project is an orchestrated data pipeline that fetches monster data from the D&D 5e API, cleans it, and saves the result as a JSON file. It was created as a MediaProbe Internship challenge.

## Technology Stack
*   **Python**
*   **Prefect**: For pipeline orchestration.
*   **Docker** & **Docker Compose**: For containerization and running services.
*   **Pydantic**: For data validation.

---

## How to Run

### Prerequisites
*   **Docker Desktop** for Windows/Mac, or Docker Engine for Linux.
*   **Git** for cloning the repository.

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
*(Note: If you are on an older system, you may need to use `docker-compose` with a hyphen.)*

You can view the Prefect dashboard at **[http://localhost:4200](http://localhost:4200)**.

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

## Output & Shutdown

*   **Output File:** After the pipeline runs, a **`monsters.json`** file will be created in your project directory.
*   **Shutting Down:** To stop and remove all containers, run:
    ```bash
    docker compose down
    ```

---

## Project Details & Requirements Checklist

- **✅ Limit fetched results via API filters or pagination**
  - The pipeline first fetches a lightweight list of all monster names, then selects a small, configurable number *before* fetching their full, detailed data. This limits the main API load to only the monsters we need.

- **✅ Make pipeline idempotent**
  - Monster selection is seeded with the current date, guaranteeing the same "random" monsters are chosen for any run on the same day. This makes the pipeline's output reproducible.

- **✅ Add CLI arguments for monster selection**
  - The `main.py` entrypoint uses Python's standard `argparse` library to accept a `--num-monsters` command-line argument, which is then passed as a parameter to the Prefect flow.

- **✅ Cache API response locally**
  - The Prefect `@task` decorator is configured with `persist_result=True` and `cache_key_fn=task_input_hash`. This automatically saves a task's output and reuses it on subsequent runs with the same inputs, preventing re-fetching of already seen monsters.

- **❌ Add unit tests for task components**
  - Unit tests would be added using `pytest` to validate the logic of individual transformation and validation tasks.

---

## Troubleshooting

### Note for Linux Users: Handling `sudo` requirement
On new Linux systems, you may need to run `docker` commands with `sudo`. This is a standard permissions issue that should be fixed with a one-time setup.

**1. Add your user to the `docker` group.**
```bash
# Creates the 'docker' group if it doesn't exist
sudo groupadd docker

# Adds your current user to the 'docker' group
sudo usmod -aG docker $USER
```

**2. IMPORTANT: Apply the new group membership.**
For the changes to take effect, you must **log out and log back in** or **reboot your system**.

**3. Verify the fix.**
After logging back in, test that you can run Docker commands without `sudo`:
```bash
docker ps
```  
