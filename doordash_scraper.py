from pydantic import BaseModel
from typing import Optional, List


class DoorDashOrder(BaseModel):
    """Represents a single DoorDash order."""
    restaurant: str
    status: str
    estimated_delivery: Optional[str] = None
    order_id: Optional[str] = None


class OrdersResult(BaseModel):
    """Result of extracting orders from the page."""
    orders: List[DoorDashOrder]
    has_active_orders: bool


async def extract_orders(page) -> OrdersResult:
    """
    Extract active orders from the current DoorDash orders page.
    Uses Stagehand's AI extraction to find order information.
    """
    
    result = await page.extract(
        instruction="""
        Look at this DoorDash orders page and extract information about any ACTIVE orders.
        Active orders are ones currently being prepared, picked up, or delivered - NOT completed/past orders.
        
        For each active order, extract:
        - restaurant: The restaurant or store name (e.g., "DashMart", "McDonald's")
        - status: The current status text (e.g., "Picking up your order", "Preparing your order", "Dasher is on the way")
        - estimated_delivery: The estimated delivery time if shown (e.g., "2:02 - 2:17 AM")
        - order_id: The order ID if visible in any links (usually a UUID like "12af70e4-2fbc-4056-8486-b6782ffa6202")
        
        If there are no active orders (only past/completed orders), return has_active_orders as false and an empty orders list.
        """,
        schema=OrdersResult
    )
    
    return result