import os
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone=utc)

@scheduler.scheduled_job('cron', hour=0)
def update_num_days_dry():
    from src.models.drinker import Drinker

    for d in Drinker.all():
        if d.is_dry():
            dry_day_count = d.num_days_dry
            print "Increasing {0}'s Dry Streak to {1} days.".format(d.name, d.num_days_dry + 1)
            d.update(num_days_dry=dry_day_count + 1)
        else:
            print "Resetting {0}'s Dry Streak to 0.".format(d.name)
            d.update(num_days_dry=0)
