# wumpus_world
An AI solution to an implementation of the Wumpus World Game

## Local development

### Requirements

- python 2.7
- unix style operating system

### Environment Setup

#### Installing virtualenv

    $ pip install virtualenv

#### Creating a virtual environment
    $ virtualenv venv
    
#### Activating your virtual environment

    $ source venv/bin/activate
    
#### Installing requirements

1. Activate your virtual environment

2. `$ pip install requirements-dev.txt`

#### Adding a git hook

This will make git run tests before you make a commit

From the root directory of your project:

    $ echo "./run-tests.sh" > .git/hooks/pre-commit
    $ chomd +x .git/hooks/pre-commit    

### Contributing

1. Create a new branch to do changes on
- Branch should be appropriately named for the changes made
2. Create a PR from your branch to master
3. After your branch receives a `+1` it can be merged
