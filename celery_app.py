from celery import Celery
from worker_deps import price_service_ctx
import asyncio
from celery.schedules import crontab

app = Celery("celery_app", broker="redis://redis:6379/0")


_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


@app.task(name="get_data_from_deribit_all")
def get_data_from_deribit_all():
    _loop.run_until_complete(_get_all())
    _loop.close()


async def _get_all():
    from worker_deps import price_service_ctx

    async with price_service_ctx() as service:
        await service.add_new_price("btc_usd")
        await service.add_new_price("eth_usd")


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(crontab(minute="*"), get_data_from_deribit_all.s())
