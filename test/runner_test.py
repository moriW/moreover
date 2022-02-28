import time
import asyncio
from moreover.base.runner import AsyncExecutor


class TaskExecutor(AsyncExecutor):
    @classmethod
    def task(cls):
        print("start", time.time())
        time.sleep(100)
        print("end", time.time())


async def main():
    await TaskExecutor.execute()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
