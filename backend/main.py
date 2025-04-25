from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.models import db
from app.tasks import full_update
from app import app

def create_app():
    # scheduler = BackgroundScheduler()
    # trigger = CronTrigger(
    #     year="*",
    #     month="*", 
    #     day="*", 
    #     hour="0", 
    #     minute="0", 
    #     timezone="US/Eastern"
    # )
    
    # scheduler.add_job(
    #     func=full_update, 
    #     trigger=trigger, 
    #     id="full_inference_job"
    # )
    
    # if not scheduler.running:
    #     scheduler.start()
    
    with app.app_context():
        db.create_all()
    
    return app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
