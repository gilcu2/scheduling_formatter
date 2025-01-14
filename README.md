# Reservation scheduling formatter



## Development

### Requirements:

* Python 3.8+
* [Poetry](https://python-poetry.org/)

### Setup

1. Get the source code
2. Install dependencies

  ```sh
  poetry install
  ```

1. Activate the virtual environment and set env vars

  ```sh
  poetry shell
  source .env
  ```

### Checks

```sh
scripts/lint.sh
scripts/type_check.sh
scripts/test.sh
```

### Run

1. In one terminal:

```sh
scripts/run_server.sh
```

1. In other terminal:

```sh
scripts/run_client.sh
```

