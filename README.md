# **Research_track_assignment_1**

## Python Simulator Robot


### **Project Description** 

The aim of this project is to pick and move all the silver tokens and release them next to the golden token. The robot also understands that the task is completed when all the tokens are in pairs. Code is written in pyhton. The initial point of the robot is not important, and this code can be applied to all initial points. 



### **Installing and running**

The simulator requires a Python 2.7 installation, the [pygame](https://www.pygame.org/news) library, [PyPyBox2D](https://pypi.org/project/pypybox2d/2.1-r331/), and [PyYAML](https://pypi.org/project/PyYAML/).

Pygame, unfortunately, can be tricky (though not impossible) to install in virtual environments. If you are using ```pip```, you might try 
```pip install hg+https://bitbucket.org/pygame/pygame```, or you could use your operating system's package manager. Windows users could use [Portable Python](https://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using ```pip``` or ```easy_install```.

* The main code is written inside the file named assignment.py. 
* In order to run the project the command below should be written in the terminal.
```
python2 run.py assignment.py
```


### **Algorithm**

The algorithm of the code is explained using the flowchart below:

<p align="center">
  <img src="https://user-images.githubusercontent.com/51851879/199999145-ff04b822-7948-423d-b552-cf03cf22fec1.jpg">
</p>


First, the robot checks the length of the token array. This array contains the gold and silver tokens that are targeted. For example, if the robot keeps a silver token and releases it next to a gold token, the offset number of these two tokens is kept in the token array. And this main loop continues until all tokens are held in this array. 

The second step depends on the length of this array. If the length is an even number, it means that the robot needs to look for a silver token, if not it looks for a golden token. When the robot detects a token, the first thing is to do is to check this token to understand if it is already targeted before. If it is the same, it turns and looks for a new token, otherwise it selects this token as the target. 

The third step depends on the type of the token. If the token is silver it goes next to it, adds its offset value to the array then grabs it. Then, it goes back to the starting point of the loop. If the token is a gold one, there is an extra control not to drag along any other silver tokens on their way. If there is another silver token on the way, the robot makes a maneuver to skip this object, then it continues its own way. When the robot brings the silver token to the golden one, it adds the offset number of this gold token to the token array, then releases the silver token next to the gold one and goes back to the starting point of the loop. This loop continues until all the tokens are targeted, which means the length of the token array is equal to 12.

### **Robot Vision**

Robot vision is used both for indicating the color type of the tokens and also for their sizes and offset values. The size of the token that is held is important when it goes toward the golden token to release it next to the golden token. In order to reach the size and offset values, the commands below are used: 

* token.info.size 
* token.info.offset

Also, the *see()* function is used to not crash to the other silver tokens on the way. Basically, this function takes the rotation angles of all silver tokens except the held one, then if the angle between the robot and any silver token is smaller than a specific angle it turns left a bit to get rid of the obstacle.

The *append()* command is also used to define the targeted tokens and not mix the token that is already paired and not touched before. It gives the opportunity to decide which type of token is needed to be looked for. 

### **Possible Improvements**

* Instead of choosing the turning angle arbitrarily, it can be calculated using robot vision. For example, if the angle between the robot and the obstacle is calculated, the robot can turn to the other side. Also, it can be used for drive commands, which are arbitrary, too. So it can update its speed for every iteration adaptively.
* Also, obstacle avoidance when the robot goes to the silver object can be added. 


##### **X4 speed video**

<div align="center">
<video src="https://user-images.githubusercontent.com/51851879/200179212-cfd08772-8069-420a-a3cc-52b33b89f074.mp4" width=400/>
