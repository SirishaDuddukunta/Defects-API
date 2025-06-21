from pydantic import BaseModel
from datetime import date

class Defect(BaseModel):
    defect_id: int
    product_id: str
    defect_type: str
    defect_description: str
    defect_date: date
    defect_location: str
    severity: str
    inspection_method: str
    repair_action: str
    repair_cost: float