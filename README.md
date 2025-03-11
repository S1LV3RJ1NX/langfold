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

- The project is divided into templates, situated in the [templates](./templates) directory. Each template has its own README.md file.

- To restart an existing template, run:

```bash
make up t=<template-folder-name>
```

- To build a new template, run:

```bash
make down t=<old-template-folder-name>
make build t=<new-template-folder-name>
```
