import asyncio


FUTURES = []


async def main():
    t = asyncio.create_task(test())
    await do_work()
    await t


async def do_work():
    futs = [frob_a_tree() for i in range(3)]
    await asyncio.gather(*futs)


async def frob_a_tree():
    await b_tree()


async def b_tree():
    f = asyncio.Future()
    FUTURES.append(f)
    t = asyncio.create_task(frob_a_branch(f))
    await asyncio.gather(t)


async def frob_a_branch(f):
    await b_branch(f)


async def b_branch(f):
    await f


def name(t):
    try:
        # Python3.8
        return t.get_name()
    except AttributeError:
        return f"Task-{id(t)}"


async def test():
    import sys

    await asyncio.sleep(0.1)
    print("### Python native")
    for t in asyncio.all_tasks():
        print(name(t))
        asyncio.base_tasks._task_print_stack(t, None, sys.stdout)
        print()

    for t in asyncio.all_tasks():
        waiter = t._fut_waiter
        """
        # FIXME waiter is not a Task, it's a:
        * _asyncio.Future
        * asyncio.tasks._GatheringFuture
        * ...
        * None
        """
        try:
            waiter = ", ".join(map(name, waiter._children))
        except AttributeError:
            pass
        print(f"{name(t)} -> {waiter}")

    # Extended stack
    # import awaitwhat

    for f in FUTURES:
        f.set_result(None)


if __name__ == "__main__":
    asyncio.run(main())
