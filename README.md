# Ontology LOTR

## Install dependencies

### Virtual Environment
```bash
python3 -m venv .venv
```

### Activate

* **Fish:**
  ```fish
  source .venv/bin/activate.fish
  ```

* **Bash or Zsh:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## Open backend

```bash
uvicorn api.server:app --reload
```