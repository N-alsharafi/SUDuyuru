# SUDuyuru
Sabanci University announcements-via-email service.  &nbsp; &nbsp;  `Current Version: 1.3.1`

This software sends the announcements made on the MySU platform via email to Sabanci University students.

&nbsp;  

## How do I get the announcements? 
If you are a student and would like to sign up or opt out (after having signed up), you can do so through [this](https://docs.google.com/forms/d/e/1FAIpQLSctaTmhUP7JPJLhNYtZJ3ArsXXdUXu4y7pcYjkQL-N_efC9yA/viewform?usp=sf_link) form. 

      
* Please note that it will take about a week or two to apply your action (sign up or opt out).

&nbsp; 

---
## Changelog:

### 1.3.1
* fixed a bug with login that was recently introduced

### new in 1.3.0:
* fixed mailing list to circumvent max recepient.

### new in 1.2.2:
* proper error handling for dbOps.connect_to_database
* proper ip resolution for accessing mongodb

### new in 1.2.1:
* added versions for packages to ensure SUDuyuru doesn't break with python package updates
* uploaded the .gitignore to github

### New in 1.2.0:
* Updated mail content and implemented more advanced html and css for formatting.

### New in 1.1.2:
* Implemented proper logging instead of print statements, info can now be viewed in docker logs while the container is running.

### New in 1.1.1:
* Fixed a bug where I put the wrong argument in the wrong function.

### New in 1.1.0:
* Added module to handle updating the client list. The filename must be added in creds.py

---

&nbsp;  

&nbsp; 

# Upcoming changes:

## Upcoming fixes/features:
* proper error handling
* important announcements section

## SUDuyuru v.2.0.
* Announcements will have attached dates
* Announcements in Turkish option
* today-on-campus daily mail
* move module design from functions to objects.


