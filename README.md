
# AirBnB Clone Project

![AirBnB](img/airbnb.png)

This project is being undertaken by The ALX School as part of their curriculum.

## Introduction

The objective of this project is to create a simplified version of the AirBnB website. While the project won't encompass all the features of the original website, it will cover essential concepts from the higher-level programming track.

## Phase 1: Development of the Command Interpreter

The primary task in this initial phase is to build a command interpreter that facilitates the management of AirBnB objects.

# What is a Command Interpreter?

In essence, a command interpreter resembles the functionality of a shell, but it's tailored to a specific use-case. For this project, the command interpreter enables us to handle various tasks related to our project objects:

0. **Creation of New Objects:** This involves generating new instances of objects like Users or Places.
1. **Retrieval of Objects:** The interpreter should allow us to retrieve objects from different sources, such as files or databases.
2. **Object Operations:** We'll be able to perform operations on objects, such as counting objects or computing statistics.
3. **Object Attribute Updates:** The interpreter will facilitate the modification of object attributes.
4. **Object Deletion:** It will be possible to remove objects from the system.

By accomplishing this phase, we'll lay a solid foundation that will be employed and expanded upon in the subsequent project phases, which include HTML/CSS templating, database storage, API integration, and front-end development.
## The Usage of the console

```bash
    $ ./console.py
    (hbnb) help

    Documented commands (type help <topic>):
    ========================================
    EOF  help  quit

    (hbnb) 
    (hbnb) 
    (hbnb) quit
$
```

**also can be used in non-interactive mod**

```bash
    $ echo "help" | ./console.py
    (hbnb)

    Documented commands (type help <topic>):
    ========================================
    EOF  help  quit
    (hbnb) 
    $
    $ cat test_help
    help
    $
    $ cat test_help | ./console.py
    (hbnb)

    Documented commands (type help <topic>):
    ========================================
    EOF  help  quit
    (hbnb) 
    $
```

## the commands that are available

## Available Commands

| Command      | Description                                      |
|:-------------|:-------------------------------------------------|
| `create`     | Create a new instance of a specified model.      |
| `all`        | List all data for the created model instances.   |
| `show`       | Display data for a specific model instance.      |
| `count`      | Count the number of instances for a model.       |
| `destroy`    | Delete a model instance by its ID.               |
| `update`     | Modify data for a specific model instance.       |
| `quit`       | Exit the console.                                |
| `help`       | List available commands or get help for a command|

