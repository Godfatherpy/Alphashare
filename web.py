import asyncio
import os
from aiohttp import web, ClientSession, ClientTimeout

async def start_webserver():
    routes = web.RouteTableDef()

    @routes.get("/", allow_head=True)
    async def root_route_handler(request):
        return web.json_response({"status": "running"})

    async def web_server():
        web_app = web.Application()
        web_app.add_routes(routes)
        return web_app

    app = web.AppRunner(await web_server())
    await app.setup()
    # Use the PORT environment variable provided by Render or default to 8080
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(app, "0.0.0.0", port).start()
    print(f"Web server started on port {port}")

async def ping_server(url, sleep_time):
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                async with session.get(url) as resp:
                    print(f"Pinged server {url} with response: {resp.status}")
        except Exception as e:
            print(f"Ping error: {e}")
