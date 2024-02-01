# SUDuyuru
---
Sabanci University announcements-via-mail service.

an extensive description will be added once there is something to describe...


### If you wish to contribute:
---
This project is built in containers so that enviroment dependencies are easily consistent.

You will need docker to run this project. You will need to have a working understanding of git, if you don't
* [this should be your first contribution](https://github.com/firstcontributions/first-contributions)

#### Getting up and running:
1. Fork the repository into your account
2. Clone the directory using
```
git clone link-to-repo/github.com
```
3. Navigate to the project folder, and create the following file
```
./src/creds.py
```
To be able to run the project, in the file you will define 3 parameters, username, password and exec. 
These are the payload parameters which you will have to obtain and add on your own.
4. Navigate to the project folder and create a new branch with the an appropriate title
```
git switch -c your-new-branch-name
```
5. Run
```
docker compose up --build
```
---
#### Important tips:
* if you add a new dependency make sure to add it in `requirements.txt`
* to stop the containers properly run `docker compose down`
* to start the containers without rebuilding the image `docker compose up`

P.S. 
* Understand the filesystem and code before writing anything
* write beautiful code (Credit to Linus Torvalds).
