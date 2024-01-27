# SUDuyuru
---
Sabanci University announcements-via-mail service.

an extensive description will be added once there is something to describe...


### If you wish to contribute:
---
This project is built in containers so that enviroment dependencies are easily consistent.

You will need docker to run this project.

#### Getting up and running:
1. clone the directory using
```
git clone link-to-repo.github.com
```
2. navigate to the project folder and run
```
docker compose up --build
```
---
#### Important tips:
* if you add a new dependency make sure to add it in `requirements.txt`
* to stop the containers properly run `docker compose down`
* to start the containers without rebuilding the image `docker compose up`

P.S. make the code as modular and single-function as possible to make future contributions easier to carry out.