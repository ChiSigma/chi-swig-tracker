import model
import event
from orator.orm import has_many


class EventType(model.Model):
	# (Name for the frontend, window for querying the db)
	COUNT_WINDOWS = [('Past Day', '12h'), ('Past Week', '7d'), ('All Time', '*')]

	@has_many
	def events(self):
		return event.Event
