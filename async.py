import os
import time
import asyncio
import aiofiles
import functools
from contextlib import contextmanager


def logger(func):
    @functools.wraps(func)
    def timer(**kwargs):
        start_time = time.time()
        r = func(**kwargs)
        print('total time cost of {}: {} second(s)。'.format(
            func.__name__, time.time() - start_time))
        return r
    return timer


@logger
def asyncfunc(**kwargs):
    async def subfunc(name: str, waittime: float):
        print('subfunc {} started.'.format(name))
        await asyncio.sleep(waittime)
        print('subfunc {} finished after {} second(s).'.format(name, waittime))

    async def loop():
        '''
        将所有协程封装为一个Task，供asyncio.run()调用执行，有asyncio.wait()和asyncio.gather()两种方法
        asyncio.wait()将所有协程组合成一个列表输入，支持设置任务结束时机(所有协程结束后返回:ALL_COMPLETED/第一个协程结束后返回:FIRST_COMPLETED/第一次异常后返回:FIRST_EXCEPTION)
        asyncio.gather()将每个协程作为单独参数输入，仅返回各个协程的执行结果，没有其余设置，用法较为简单，可以满足大部分使用场景
        '''
        await asyncio.wait([subfunc(arg, kwargs[arg]) for arg in kwargs], return_when='ALL_COMPLETED')
        # await asyncio.gather(*[subfunc(arg, kwargs[arg]) for arg in kwargs])

    asyncio.run(loop())


@logger
def quenefunc(**kwargs):
    def subfunc(name: str, waittime: float):
        print('subfunc {} started.'.format(name))
        time.sleep(waittime)
        print('subfunc {} finished after {} second(s).'.format(name, waittime))

    for arg in kwargs:
        subfunc(arg, kwargs[arg])


@logger
def asyncfileio(**kwargs):
    async def file_write(filename: str, text: str):
        async with aiofiles.open(os.path.dirname(__file__) + f'/{filename}.txt', 'w', encoding="utf-8") as f:
            await f.write(text)

    async def loop():
        await asyncio.wait(*[file_write(arg, kwargs[arg]) for arg in kwargs])

    asyncio.run(loop())


@logger
def quenefileio(**kwargs):
    def file_write(filename: str, text: str):
        with open(os.path.dirname(__file__) + f'/{filename}.txt', 'w', encoding="utf-8") as f:
            f.write(text)

    for arg in kwargs:
        file_write(arg, kwargs[arg])


if __name__ == '__main__':
    asyncfunc(a=10, b=2, c=3, d=4, e=5, f=0)
    quenefunc(a=10, b=2, c=3, d=4, e=5, f=0)
    # asyncfileio(a='a\n'*100000, b='a\n'*500000, c='a\n'*1000000)
    # quenefileio(d='a\n'*100000, e='a\n'*500000, f='a\n'*1000000)
