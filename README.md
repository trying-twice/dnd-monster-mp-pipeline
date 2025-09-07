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
This command starts the Prefect server and database in the background.```bash
docker-compose up -d
```
You can view the Prefect dashboard at [http://localhost:4200](http://localhost:4200).

### 3. Run the Pipeline
Execute the pipeline inside the running container.

**To run with the default of 5 monsters:**
```bash
docker-compose exec prefect-server python src/main.py
```

**To specify a different number of monsters:**
```bash
docker-compose exec prefect-server python src/main.py --num-monsters 15
```

---

## Output
After the pipeline runs, you will find a **`monsters.json`** file in your project directory containing the final data.

## Shutting Down
To stop and remove the containers, run:
```bash
docker-compose down
```