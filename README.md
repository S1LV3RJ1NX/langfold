# LangFold

## What is LangFold?

LangFold is a production grade scaffolding framework for building LLM powered agents with Langraph.

## Setup

- Install uv: https://docs.astral.sh/uv/getting-started/installation/

- Sync the project dependencies

```bash
uv sync
```

- For first time:

  - setup pre-commit hooks

    ```bash
    pre-commit install
    ```

  - run pre-commit hooks

    ```bash
    pre-commit run --all-files
    ```

## Execute

```bash
uvicorn src.main:app --host 0.0.0.0 --port 21120 --reload
```

- This builds the workflow graph from [agent.yaml](./config/agent.yaml) and starts the FastAPI server at port 21120
