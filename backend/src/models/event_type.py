import model
import event
from orator.orm import has_many

class EventType(model.Model):
	@has_many
	def events(self):
		return event.Event
