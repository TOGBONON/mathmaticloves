from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🔥 WebSocket connect attempt")
        user = self.scope["user"]

        if user.is_anonymous:
            print("❌ Anonymous user")
            await self.close()
            return

        # Group name = user_{id}
        self.group_name = f"user_{user.id}"

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        print("✅ Connected to group:", self.group_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # 🔥 This matches "type": "incoming_call"
    async def incoming_call(self, event):
        await self.send(text_data=json.dumps({
            "type": "incoming_call",
            "call_id": event["call_id"],
            "student_name": event["student_name"],
        }))