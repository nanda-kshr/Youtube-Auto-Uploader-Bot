from apscheduler.schedulers.blocking import BlockingScheduler

def schedule_tasks():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_bot, 'interval', hours=1)  # Run every 1 hour
    scheduler.start()

def run_bot():
    browser = setup_browser()
    login(browser, "my-username", "my-password")
    upload_short(browser, "path/to/video")
    browser.quit()

if __name__ == "__main__":
    schedule_tasks()
