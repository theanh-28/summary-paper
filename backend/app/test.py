import asyncio

async def task():
    await asyncio.sleep(3)
    print("Xong task")

async def main():
    await task()
    print("Tiếp tục")

asyncio.run(main())