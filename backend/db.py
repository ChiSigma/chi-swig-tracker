from src import app as init_app

if __name__ == "__main__":
	db = init_app.db
	db.cli.run()
