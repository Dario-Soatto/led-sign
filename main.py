import asyncio
from playwright.async_api import async_playwright
import anthropic
import config
import json
import os
from led_controller import send_to_led

LOOP_INTERVAL = 10  # seconds between checks


async def scrape_orders(page, client):
    """Scrape and parse orders from the current page."""
    
    page_text = await page.evaluate("document.body.innerText")
    
    order_html = await page.evaluate("""
        () => {
            const viewOrderBtns = document.querySelectorAll('[aria-label="View Order"]');
            const viewReceiptBtns = document.querySelectorAll('[aria-label="View Receipt"]');
            let result = "=== ACTIVE ORDERS ===\\n";
            viewOrderBtns.forEach((el, i) => {
                const card = el.closest('div[class*="Container"]');
                result += `Active ${i+1}: ${card?.innerText || 'N/A'}\\n---\\n`;
            });
            result += "\\n=== DELIVERED ORDERS ===\\n";
            viewReceiptBtns.forEach((el, i) => {
                const card = el.closest('div[class*="Container"]');
                result += `Delivered ${i+1}: ${card?.innerText || 'N/A'}\\n---\\n`;
            });
            return result;
        }
    """)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Extract from DoorDash orders page:

1. ACTIVE ORDERS (being prepared/delivered): restaurant, status, ETA
2. 3 MOST RECENT DELIVERED: restaurant name only

JSON format:
{{"active_orders": [{{"restaurant": "...", "status": "...", "estimated_delivery": "..."}}], "recent_delivered": [{{"restaurant": "..."}}]}}

Page content:
{page_text[:3000]}

Order cards:
{order_html[:3000]}"""
        }]
    )
    
    response_text = message.content[0].text
    
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        return json.loads(response_text[start:end])
    except json.JSONDecodeError:
        return None


def format_led_message(data):
    """Format order data into a message for the LED sign."""
    if not data:
        return "No orders"
    
    active = data.get("active_orders", [])
    delivered = data.get("recent_delivered", [])
    
    lines = []
    
    # Active orders with ETA time range
    for o in active:
        restaurant = o.get('restaurant', '?')
        eta = o.get('estimated_delivery', '')
        if eta:
            # Clean up the ETA - extract just the time range
            # Remove date parts like "Dec 18," and keep times
            import re
            times = re.findall(r'\d{1,2}:\d{2}', eta)
            if len(times) >= 2:
                lines.append(f"{restaurant}: {times[0]}-{times[1]}")
            elif len(times) == 1:
                lines.append(f"{restaurant}: {times[0]}")
            else:
                lines.append(f"{restaurant}: {eta}")
        else:
            lines.append(f"{restaurant}: In progress")
    
    # Delivered orders - each with ": Delivered"
    for o in delivered[:3]:
        restaurant = o.get('restaurant', '?')
        lines.append(f"{restaurant}: Delivered")
    
    if not lines:
        return "No orders"
    
    return "\n".join(lines)


async def main():
    print("=" * 50)
    print("DoorDash LED Monitor")
    print("=" * 50)
    
    print("\n⚠️  CLOSE ALL CHROME WINDOWS FIRST!")
    input("Press Enter once Chrome is closed...")
    
    profile_dir = os.path.join(os.path.dirname(__file__), "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    
    print(f"\n📁 Using profile: {profile_dir}")
    print("🚀 Launching Chrome...")
    
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="chrome",
            headless=False,
            slow_mo=50,
            timeout=60000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--disable-sync",
            ],
        )
        print("   ✅ Chrome launched!")
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("📦 Navigating to DoorDash orders...")
        await page.goto(config.DOORDASH_ORDERS_URL, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Check if we need to log in
        if "login" in page.url.lower() or "identity" in page.url.lower():
            print("\n" + "=" * 50)
            print("👤 PLEASE LOG IN TO DOORDASH")
            print("   Log in using the browser window")
            print("   Then press Enter here when done...")
            print("=" * 50)
            input()
            await page.goto(config.DOORDASH_ORDERS_URL, wait_until="domcontentloaded")
            await asyncio.sleep(3)
        
        print(f"\n🔄 Starting monitoring loop (every {LOOP_INTERVAL}s)")
        print("   Press Ctrl+C to stop\n")
        
        loop_count = 0
        
        try:
            while True:
                loop_count += 1
                print(f"--- Loop #{loop_count} ---")
                
                # Refresh the page
                print("🔄 Refreshing page...")
                await page.reload(wait_until="domcontentloaded")
                await asyncio.sleep(3)
                
                # Scrape orders
                print("🔍 Scraping orders...")
                data = await scrape_orders(page, client)
                
                if data:
                    # Print results
                    active = data.get("active_orders", [])
                    delivered = data.get("recent_delivered", [])
                    
                    if active:
                        print(f"   🔴 Active: {len(active)} order(s)")
                        for o in active:
                            print(f"      - {o.get('restaurant')}: {o.get('status')}")
                    else:
                        print("   📭 No active orders")
                    
                    # Format and send to LED
                    led_message = format_led_message(data)
                    print(f"📺 LED: {led_message}")
                    
                    send_to_led(led_message)
                else:
                    print("   ❌ Failed to parse orders")
                
                print(f"⏳ Waiting {LOOP_INTERVAL}s...\n")
                await asyncio.sleep(LOOP_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping...")
        
        await context.close()
    
    print("👋 Done!")


if __name__ == "__main__":
    asyncio.run(main())