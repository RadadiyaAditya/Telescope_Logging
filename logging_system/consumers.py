"""
WebSocket consumer to broadcast Local Sidereal Time (LST) and UTC time in real-time.

Uses Django Channels' AsyncWebsocketConsumer to:
- Send LST and UTC time every second
- Handle graceful disconnection

Imports:
- `compute_lst` from `lst.py` for real-time sidereal calculations
"""

import json
import asyncio
from datetime import datetime, timezone
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .lst import compute_lst
logger = logging.getLogger(__name__)

class LSTConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer that continuously sends current Local Sidereal Time (LST)
    and Coordinated Universal Time (UTC) to connected clients every second.

    This is useful for astronomical interfaces needing real-time sky tracking.
    """

    async def connect(self):
        """
        Called when a WebSocket connection is initiated.
        Accepts the connection and starts sending LST + UTC time every second.
        """
        await self.accept()

        while True:
        # Get current UTC and LST time (computed from system time)
            lst_time = compute_lst()  # Get updated LST
            utc_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Send times as a JSON payload
            await self.send(json.dumps({"lst_time": lst_time, "utc_time": utc_time}))
            await asyncio.sleep(1)  # Send update every second

            
    async def disconnect(self, close_code):
        """
        Called when the WebSocket connection is closed.
        Attempts to remove the client from any groups (if used in the future).

        Args:
            close_code (int): Close code for the connection.
        """
        try:
            # Perform cleanup tasks
            await self.channel_layer.group_discard("lst_group", self.channel_name)
        except Exception as e:
            logger.error(f"Error in disconnect: {e}")
        finally:
            await super().disconnect(close_code)

class SerialConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("serial_data", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("serial_data", self.channel_name)

    async def serial_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))