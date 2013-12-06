# let's**do**

[Let's**do**](http://lets-do.herokuapp.com) is a social task manager webapp. It was written for Case Western Reserve University EESC 393 Project by Wes Rupert, Shelley Murphy and Charles Marshall. Project is written in HMTL/Django and intended for mobile platforms.


# User Manual
---
User's Manual for let's do
Charles Marshall, Shelley Murphy, Wes Rupert

## Creating a new user
When first coming to the site, you are prompted for your username and password. Assuming this is your first time on the site, you will need to make a new profile. The text at the bottom that says “Sign up now” is a link that, when clicked, will take you to a registration page. You will need to provide all the information requested, then click the button that says “Sign up” to register your account.

## Logging on
From the login screen, enter your username and password and click log in to log in.
Creating a new task list
At the top center of the screen is a small plus sign. Click it to be redirected to the new task page. You must enter information for the title and description, but the other information may be left blank if you choose. Click the “Save List” button to save the list.

## Viewing a task list
To see the tasks in a task list, click on the title of the list. The tasks will be brought up for use.

## Editing a task list
To edit a task list, make sure you are on its page, before going to the right of the screen and pressing the edit button

## Deleting a task list
On your homepage, find the task list you wish to delete. On the right of the screen, there is an X at the level of the task list. Clicking this will delete the task list.
Creating new tasks
While viewing the tasks in the task list you wish to add a task to, click the small plus sign in the top middle of the screen. You will be taken to a new task page. The title and description of the task are required, but the category and due date can be left off if desired. Click “Save Task” to save your task and see it show up as a task on your current task list.

## Tasks with due dates
If a task is given a due date, tasks will be listed with the soonest due date listed first. If a task is due today or late, it will be listed in red. 

## Task Status
To mark a task as complete, click the empty circle next to it. To mark it as still in progress again, click the circle again

## Editing Tasks
For each task, on the right of the screen, there is an edit button. Clicking this will take you to an edit page.

## Deleting Tasks
For each task, on the right of the screen, there is an X. Clicking this will delete the task.

## Sharing Lists
On the page of the list you want to share, click the share button on the far right. You will be given the option to share the list with any users in the system, and what level of control you want to give them.

## User levels of editing rights
When a list is shared with a user, if they are given the right to edit, they will be able to add tasks and mark them as complete. If they are not, they will only be able to view all the tasks and the statuses of them.


# Testing report
---
    Name           Stmts   Miss  Cover   Missing
    --------------------------------------------
    tasks              0      0   100%   
    tasks.admin        9      0   100%   
    tasks.forms       25      0   100%   
    tasks.models      61      2    97%   27, 66
    tasks.urls         3      0   100%   
    tasks.views      160     98    39%   29-46, 56-61, 80-93, 109-116, 133, 138-146, 160-179, 184-208, 213-221, 227-237, 242-248
    --------------------------------------------
    TOTAL            258    100    61%   
    ----------------------------------------------------------------------
    Ran 27 tests in 10.945s

    OK
    nosetests --with-coverage --cover-package=tasks --verbosity=1
    Creating test database for alias 'default'...
    Destroying test database for alias 'default'...
