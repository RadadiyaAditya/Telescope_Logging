import json
import asyncio
from datetime import datetime, timezone
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .lst import compute_lst
logger = logging.getLogger(__name__)

class LSTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            lst_time = compute_lst(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")  # Get updated LST
            utc_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
  # Get current UTC time
            await self.send(json.dumps({"lst_time": lst_time, "utc_time": utc_time}))
            await asyncio.sleep(1)  # Send update every second
    async def disconnect(self, close_code):
        try:
            # Perform cleanup tasks
            await self.channel_layer.group_discard("lst_group", self.channel_name)
        except Exception as e:
            logger.error(f"Error in disconnect: {e}")
        finally:
            await super().disconnect(close_code)