import streamlink
import asyncio
import sys
import websockets

async def stream():
    async with websockets.connect(
        "wss://api.deepgram.com/v1/listen",
        extra_headers={
            "Authorization": "Token {}".format("DEEPGRAM_API_KEY")
        },
    ) as ws:
        async def sender(ws):
            url = "https://www.youtube.com/watch?v=iIg9gI_AZwM"
            streams = streamlink.streams(url)
            f = streams["worst"].open()
            while True:
                data = f.read(4096)
                await asyncio.sleep(0.1)
                await ws.send(data)
            #unreachable
            #await ws.send(json.dumps({"type": "CloseStream"}))
            #f.close()
            #return

        async def receiver(ws):
            async for msg in ws:
                print(msg)
            return

        functions = [
            asyncio.ensure_future(sender(ws)),
            asyncio.ensure_future(receiver(ws)),
        ]
        await asyncio.gather(*functions)

def main():
    try:
        asyncio.get_event_loop().run_until_complete(stream())
    except websockets.exceptions.InvalidStatusCode as e:
        print("Failed")

if __name__ == "__main__":
    sys.exit(main() or 0)
