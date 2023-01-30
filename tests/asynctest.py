# -*- coding: UTF-8 -*-

#
# @copyright Copyright © 2018 - 2023 by Edward K Thomas Jr
# @license GNU GENERAL PUBLIC LICENSE https://www.gnu.org/licenses/gpl-3.0.en.html
#

import asyncio
import random


class test:
    def __init__(self) -> None:
        self.test = False
        self.testernum = 0

    async def nested(self, n):
        print(f"#{n} started")
        await asyncio.sleep(random.random() * 10)
        print(f"#{n} am done, test: {self.get_test()}")
        self.set_test()

    async def tester(self):
        while self.testernum < 300000:
            print(f"Counter: {self.testernum}, bool: {self.test}")
            await asyncio.sleep(0)
            self.testernum += 1

    async def main(self):

        # Schedule nested() to run soon concurrently
        # with "main()".
        task1 = asyncio.create_task(self.nested(1))
        task2 = asyncio.create_task(self.nested(2))
        task3 = asyncio.create_task(self.tester())

        # "task" can now be used to cancel "nested()", or
        # can simply be awaited to wait until it is complete:
        await asyncio.wait([task1, task2, task3])

    def run(self):
        asyncio.run(self.main())

    def set_test(self):
        self.test = True

    def get_test(self):
        return self.test


obj = test()
obj.run()
