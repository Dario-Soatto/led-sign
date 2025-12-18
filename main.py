import asyncio
from playwright.async_api import async_playwright
import anthropic
import config
import json
import os


async def main():
    print("=" * 50)
    print("DoorDash Order Monitor")
    print("=" * 50)
    
    print("\n⚠️  CLOSE ALL CHROME WINDOWS FIRST!")
    input("Press Enter once Chrome is closed...")
    
    # Use a dedicated profile in our project folder
    profile_dir = os.path.join(os.path.dirname(__file__), "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    
    print(f"\n📁 Using profile: {profile_dir}")
    print("🚀 Launching Chrome...")
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="chrome",  # Use your installed Chrome
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
        
        print(f"📄 Current URL: {page.url}")
        print("🔍 Extracting page content...")
        
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
        
        print("\n🤖 Asking Claude to parse orders...")
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
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
            data = json.loads(response_text[start:end])
            
            print("\n" + "=" * 50)
            print("📋 RESULTS")
            print("=" * 50)
            
            active = data.get("active_orders", [])
            if active:
                print(f"\n🔴 ACTIVE ORDERS ({len(active)}):")
                for i, o in enumerate(active, 1):
                    print(f"\n  #{i} {o.get('restaurant', 'Unknown')}")
                    print(f"      Status: {o.get('status', 'Unknown')}")
                    print(f"      ETA: {o.get('estimated_delivery', 'Not shown')}")
            else:
                print("\n📭 No active orders")
            
            delivered = data.get("recent_delivered", [])
            if delivered:
                print(f"\n✅ RECENT DELIVERED ({len(delivered)}):")
                for i, o in enumerate(delivered, 1):
                    print(f"  #{i} {o.get('restaurant', 'Unknown')}")
            else:
                print("\n📭 No delivered orders found")
                
        except json.JSONDecodeError as e:
            print(f"Parse error: {e}")
        
        print("\n" + "=" * 50)
        input("Press Enter to close browser...")
        await context.close()
    
    print("\n👋 Done!")


if __name__ == "__main__":
    asyncio.run(main())