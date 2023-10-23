import config
import requests
import smtplib
import json
import time
from email.message import EmailMessage

class mailserver:
    user = config.user
    pssw = config.pssw
    srvr = config.srvr
    host = config.host
    port = 587
    send = config.send
    recp = config.recp
    cryp = 'STARTTLS'

    def sendMail(sender, recipient, jobName, filamentUsed, totalTime):
        message = EmailMessage()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = "Printjob done: " + jobName
        message.set_content("Printjob " + jobName + " done in " + totalTime + ". " + str(filamentUsed) + " meters of filament used.")

        m = smtplib.SMTP(mailserver.srvr,mailserver.port)
        m.set_debuglevel(0)
        m.ehlo()
        m.starttls()
        m.login(mailserver.user,mailserver.pssw)
        m.send_message(message)
        m.quit

class printer:
    server = 'http://' + mailserver.host

class printerRequests:
    def getLatestJob(server):
        job = json.loads(requests.get(printer.server + "/server/history/list?limit=1").text)['result']['jobs'][0]
        return job
    def getJobById(server, jobId):
        job = json.loads(requests.get(printer.server + "/server/history/job?uid=" + jobId).text)['result']['job']
        return job

    def jobCrawler():
        latestJob = printerRequests.getLatestJob(printer.server)['job_id']
        job = printerRequests.getJobById(printer.server, latestJob)
        if job['status']=='in_progress':
            jobDetails = printerRequests.getJobById(printer.server, job['job_id'])
            while(jobDetails['status']=='in_progress'):
                jobDetails = json.loads(requests.get(printer.server + "/server/history/job?uid=" + job['job_id']).text)['result']['job']
                print(jobDetails['status'])
                time.sleep(60)
            filamentUsed = round(jobDetails['filament_used']/1000,2)
            totalTime = round(jobDetails['total_duration']/60,0)
            restMinutes = totalTime%60
            totalHours = int((totalTime-restMinutes)/60)
            if totalTime-restMinutes<60:
                timeMessage = str(int(restMinutes)) + " minutes"
            elif totalHours == 1:
                timeMessage = str(totalHours) + ' hour and ' + str(int(restMinutes)) + " minutes"
            else:
                timeMessage = str(totalHours) + ' hours and ' + str(int(restMinutes)) + " minutes"

            mailserver.sendMail(mailserver.send, mailserver.recp, jobDetails['filename'], filamentUsed, timeMessage)

while True:
    printerRequests.jobCrawler()
    time.sleep(30)
