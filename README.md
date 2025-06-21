# Defect Explorer API

## Project Structure
- `app/` - API logic, data processing
- `tests/` - Unit tests for endpoints
- `pipeline.yaml` - CI setup
- `Dockerfile` - Container definition

## Setup & Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
uvicorn app.main:app --reload
```

3. Docker:
```bash
docker build -t defect-api .
docker run -p 8000:8000 defect-api
```

## Example API Usage

### `/products`
```json
{"products": ["P001", "P002"]}
```

### `/defects?products=P001&from_date=2023-01-01`
```json
[
  {
    "defect_id": 1,
    "product_id": "P001",
    "defect_type": "cosmetic",
    ...
  }
]
```

### `/summary`
```json
[
  {
    "product_id": "P001",
    "total_defects": 10,
    "total_repair_cost": 5200.0,
    "minor": 4,
    "critical": 6
  }
]
```
