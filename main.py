from Bot import Bot

if __name__ == "__main__":
    bot = Bot("Short", 250, 20, 2, 10, 0.2) # only see current and next platform, 0.2 entropy
    bot.train(10000,10,True)
    bot.meta.watch()
    