import os
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone=utc)

@scheduler.scheduled_job('cron', hour=4)
def update_num_days_dry():
    from src.models.event import Event
    from src.models.drinker import Drinker
    wet_drinkers = set(Event.where('event_type_id', '=', 1).created_within('24h').pluck('drinker_id'))

    for d in Drinker.all():
        if d.id not in wet_drinkers:
            dry_day_count = d.num_days_dry + 1
            print "Increasing {0}'s Dry Streak to {1} days.".format(d.name, dry_day_count)
            d.update(num_days_dry=dry_day_count)

            if dry_day_count > d.max_days_dry:
            	d.update(max_days_dry=dry_day_count)
        else:
            print "Resetting {0}'s Dry Streak to 0.".format(d.name)
            d.update(num_days_dry=0)
