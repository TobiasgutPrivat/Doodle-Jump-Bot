from Bot import Bot

if __name__ == "__main__":
    bot = Bot("Short", 250, 20, 2, 10, 0.1) # only see current and next platform, 0.2 entropy
    bot.train(1000000,1,True)
    bot.meta.watch(500000, None)
    