# import datetime
# import celery
#
#
# # here we assume we want it to be run every 1 min(s)
# @celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1))
# def myTask():
#     # Do something here
#     # like accessing remote apis,
#     # calculating resource intensive computational data
#     # and store in cache
#     # or anything you please
#     print('This wasn\'t so difficult')
#
#
# if __name__ == "__main__":
#     myTask()
