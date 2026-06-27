# Ontology LOTR

## Setup

### Create virtual environment
```bash
make venv
```

### Activate virtual environment

* **Fish:**
  ```fish
  source .venv/bin/activate.fish
  ```

* **Bash or Zsh:**
  ```bash
  source .venv/bin/activate
  ```

### Install dependencies
```bash
make install
```

## Run

```bash
make run
```

## Reset database

Restores the database to its original state from the seed file.

```bash
make reset-db
```

## Test endpoints

Install the **REST Client** extension in VS Code (`humao.rest-client`), then open `requests.http` and click **Send Request** above any endpoint.
