# scheduling_formatter

## Installation

```sh
pip install scheduling_formatter
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

## Data representation

The input data to the app can be done in any of the serialization formats beside JSON 
like YAM, Pickle, Parquet, etc. Each of these formats have advantages and disadvantages
so selecting the one to use depends on the characteristics of the problem.
For example:
 - CSV is more compact but only does not allow complex structured data and is less standardized 
 - YAML is more readable by humans, less bureaucratic but less compact than JSON
 - Parquet with compression is high compact and query efficient but is not human-readable
 - Avro supports versioning, so is interesting to use if the data scheme change in the life 
of the app.

In our case, efficient is an important point but also is important the human readability 
and library support, so I would keep JSON as the best data format in the problem 
given the knowledge available. For example, if the application is going to serve 
thousands of restaurant I would provide an endpoint that support and array os restaurant schedules
using compressed AVRO because avoid the call for each restaurant, can be compressed 
and the schema can evolve.