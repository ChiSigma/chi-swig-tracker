from src import app as init_app

if __name__ == "__main__":
	app = init_app.app
	app.run(port=app.config['PORT'], host=app.config['HOST'])