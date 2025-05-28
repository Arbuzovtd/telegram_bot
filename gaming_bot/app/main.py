import asyncio
from aiogram import Bot, Dispatcher

from .core.config import load_config
from .bot.handlers.common.registration import router as registration_router


def main() -> None:
    config = load_config()
    if not config.token:
        raise RuntimeError('TOKEN is not set')
    bot = Bot(config.token)
    dp = Dispatcher()
    dp.include_router(registration_router)

    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
