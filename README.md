# klipper-mailbot

## Why?
As an non-telegram-user I wished to also recieve a notification, when my print is ready. For this reason I'm developing this docker-container.

## Configuration
It's as simple as cloning the repository with 
`git clone git@github.com:dbse777/klipper-mailbot.git`
 in your working directory. Just add an additional file named > config.py with the following contents (all variables are required):

user = username to log onto your mailbox   
pssw = your app specific password   
srvr = smtp server of your mailprovider   
send = mailadress from which you want to send mails   
recp = mailadress on which you want to recieve mails   
host = your klipper instance   

After creating your config-file, you can get the container up with `docker compose up -d` and should get the output:  
> Service started, waiting for print to start...
