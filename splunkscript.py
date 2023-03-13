import splunklib.client as client
import splunklib.results as results
import time

# Connect to Splunk instance
HOST = "localhost"
PORT = 8089
USERNAME = "admin"
PASSWORD = "changeme"
SERVICE = client.connect(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)

# Define search query and search parameters
QUERY = "index=myapp | stats count by status"
SEARCH_PARAMETERS = {"exec_mode": "blocking"}

# Define alert settings
ALERT_NAME = "My App Error Alert"
ALERT_CONDITION = "count > 10"
ALERT_TRIGGER = "cron"
ALERT_SCHEDULE = "*/10 * * * *"
ALERT_ACTION = "email"
ALERT_EMAIL_RECIPIENT = "admin@example.com"
ALERT_EMAIL_SUBJECT = "My App Error Alert"

# Run search query
job = SERVICE.jobs.create(QUERY, **SEARCH_PARAMETERS)
while not job.is_done():
    time.sleep(1)
if job["isDone"] == "1" and job["resultCount"] > 0:
    results_reader = results.ResultsReader(job.results())
    for result in results_reader:
        if "count" in result and result["count"] > 10:
            # Set up alert and notification
            alert = SERVICE.alerts.create(ALERT_NAME, ALERT_CONDITION, ALERT_TRIGGER, ALERT_SCHEDULE)
            alert.actions[ALERT_ACTION].enabled = True
            alert.actions[ALERT_ACTION].set_param("sendemailto", ALERT_EMAIL_RECIPIENT)
            alert.actions[ALERT_ACTION].set_param("subject", ALERT_EMAIL_SUBJECT)
            alert.update()

# Disconnect from Splunk instance
SERVICE.logout()
