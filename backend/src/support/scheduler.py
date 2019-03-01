import os
from time import sleep
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone=utc)

@scheduler.scheduled_job('cron', hour=4)
def update_drinkers_num_days_dry():
    from src.models.event import Event
    from src.models.drinker import Drinker
    wet_drinkers = set(Event.where('event_type_id', '=', 1).created_within('24h').lists('drinker_id'))

    for d in Drinker.all():
        try:
            with Drinker.transaction():
                if d.id not in wet_drinkers:
                    dry_day_count = d.num_days_dry + 1
                    total_day_count = d.total_days_dry + 1
                    print "Increasing {0}'s Dry Streak to {1} days.".format(d.name, dry_day_count)
                    d.update(_unsafe=True, num_days_dry=dry_day_count, total_days_dry=total_day_count)

                    if dry_day_count > d.max_days_dry:
                        d.update(_unsafe=True, max_days_dry=dry_day_count)
                else:
                    print "Resetting {0}'s Dry Streak to 0.".format(d.name)
                    d.update(_unsafe=True, num_days_dry=0)
            sleep(2)
        except:
            print "hitting error with updating Drinker {0}".format(d.id)


@scheduler.scheduled_job('cron', hour=4, minute=15)
def update_groups_num_days_dry():
    from src.models.event import Event
    from src.models.group import Group
    wet_drinkers = set(Event.where('event_type_id', '=', 1).created_within('24h').lists('drinker_id'))

    for g in Group.with_('primary_memberships').get():
        drinkers = set(g.primary_memberships.lists('drinker_id'))
	try:
            with Group.transaction():
                if len(drinkers.intersection(wet_drinkers)) == 0:
                    dry_day_count = g.num_days_dry + 1
                    total_day_count = g.total_days_dry + 1
                    print "Increasing {0}'s Dry Streak to {1} days.".format(g.name, dry_day_count)
                    g.update(_unsafe=True, num_days_dry=dry_day_count, total_days_dry=total_day_count)

                    if dry_day_count > g.max_days_dry:
                        g.update(_unsafe=True, max_days_dry=dry_day_count)
                else:
                    print "Resetting {0}'s Dry Streak to 0.".format(g.name)
                    g.update(_unsafe=True, num_days_dry=0)
            sleep(2)
	except:
	    print "hitting error with updating Group {0}".format(g.id)
