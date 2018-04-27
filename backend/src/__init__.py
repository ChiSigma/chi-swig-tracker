import os
import ConfigParser

if not os.path.isfile('.env'): print 'No env. vars found.'

config = ConfigParser.ConfigParser()
config.read('.env')
env_vars = config.items('ENV_VARS')
postgres = config.items('POSTGRES')
auth = config.items('AUTH')

for ev in env_vars + postgres + auth:
	os.environ[ev[0].upper()] = ev[1]
