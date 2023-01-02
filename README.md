
# Mercari Deals Finder
##  2 Jaunary 2023
#### Slail Billicko Jean Pierre

##### External Libraries used: <a href = "https://pypi.org/project/selenium/" >Selenium</a>, <a href= "https://pypi.org/project/discord-webhook/">Discord-Webhooks</a>
##### Internal Libraries used: <em>UnitTest, Time</em>

## Project Description
Created a selenium bot that mimic a user's behavior on entering Mercari.com, searching for an item, applying filters on searched items like newest first or best matches, then the bot perdioically waits and refresh the driver and if the most recent item is changed, it captures the link and sends it to a discord webhook so that the newly listed item can be viewed on discord.
***    

## Program Design
• Set up was with a basic UNIT-testing Framework provided for Python Selenium on the documentation. As mentioned on the documentation: 

A page object represents an area where the test interacts within the web application user interface. Benefits of using page object pattern:
  * Easy to read test cases
  * Creating reusable code that can share across multiple test cases
  * Reducing the amount of duplicated code
  * If the user interface changes, the fix needs changes in only one place
  
 Read more: https://selenium-python.readthedocs.io/page-objects.html#
 
 ## Video Demostration - Speed Up

https://user-images.githubusercontent.com/57454628/210282707-8d9b262f-00bd-4a83-b26c-89e512145545.mp4
