# Awful Chat

Quite literally the worst chat program of all time.
It allows and encourages XSS, it works using server side events, so no Microsoft Edge support, it doesn't work very well on mobile, and ignores absolutely all design and safety best practices.

Fun Fact:
To allow XSS, I actively had to unescape the strings in python, because post requests escape "dangerous characters" as url encoded strings.

This project depends on:
`flask redis gevent gunicorn`
And is only compatible with Linux systems.
To run the project:
Make sure redis-server is running, then run
`gunicorn --worker-class=gevent app:app`
The chat program will then host on port 80
