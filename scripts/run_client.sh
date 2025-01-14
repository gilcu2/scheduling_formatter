#!/bin/bash

curl -X POST http://127.0.0.1:8000/format_scheduling \
     -H "Content-Type: application/json" \
     -d '{
        "monday": [
            { "type":"open", "value":32400},
            { "type":"close", "value":72000}
        ]
    }'
