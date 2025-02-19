import json
import asyncio
from datetime import datetime, timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .lst import compute_lst

class LSTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            lst_time = compute_lst(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")  # Get updated LST
            utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            await self.send(json.dumps({"lst_time": lst_time, "utc_time": utc_time}))
            await asyncio.sleep(1)  # Send update every second
