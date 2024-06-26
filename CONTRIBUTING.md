# If you wish to contribute:

You can contribute in one of two ways:

1. You can inform us about issues you'd like to see fixed, or features that would enrich the experience by opening an issue ticket from the ***Issues*** tab. &nbsp; *(issues without proper descriptions will be ignored)*
2. You can work on your own issue and submit a solution. &nbsp; *(Refer to section on pull requests for details)*

&nbsp;  

## If you chose option 2:

This project is built using docker containers so that environment dependencies are easily kept consistent.

You will need Docker to run this project. You will also need to have a working understanding of git. 

If you don't:
* [this should be your first contribution](https://github.com/firstcontributions/first-contributions)

&nbsp;

### Pull requests:

For your pull request to be approved, it has to:
1. contain meaningful changes to the project
2. have proper and informative comments
3. have a detailed description of the change and improvement it brings

P.S. These rules are only meant to guide you, not limit us.

### Getting up and running:
1. Fork the repository into your account
2. Clone the directory using `git clone https://github.com/N-alsharafi/SUDuyuru`
3. Navigate to the project folder, and create the following file
```
./src/creds.py
```
To be able to run the project, in `creds.py` you will define 7 parameters:
1. username
2. password
3. exec
4. port
5. email_server
6. email_address
7. email_password
8. filename

These parameters you will have to obtain and add on your own.

8. In the project folder, create a new branch with a fitting title
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
  * This should be the command you often use instead of `docker compose up --build`
  * If you don't want container logs in your terminal, use `-d` flag
* mongoDB will create a directory called data in which it will store all it's files,
    if it fails to create the file, you might have to create it manually `./data/db/`

Finally,
- Understand the code before changing or adding.
- have good taste [(Torvalds, 2016)](https://youtu.be/o8NPllzkFhE?si=TZurusgJ8xs1UhSb&t=857)


&nbsp;