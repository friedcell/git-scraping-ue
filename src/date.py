import datetime

if __name__ == "__main__":
	now = datetime.datetime.utcnow()
	print("{}+00:00".format(now.strftime("%Y-%m-%d %H:%M:%S")))
	
