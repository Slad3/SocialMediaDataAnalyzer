# Social Media User Data Analyzer
Server for analyzing downloadable Social Media user data.

You can download your Social Media user data here:
 
 Facebook: https://www.facebook.com/dyi/?referrer=ayi 

 Instagram: https://www.instagram.com/download/request/

## Overall Process
 When the user uploads the zip file provided by given social media platform, the server unzips the file into a temporary directory on the server.
    
 Once the process finishes and is analyzed, the temporary directory is deleted along with any user data that was provided or processed during that session. No user data will be saved, everything is deleted immediately.

## Analysis

 The end goal of each analysis is to provide a json format that can be easily readable by a frontend service, whether that's the website frontend or 

### Searches
  The end result of analyzing the searches will be a JSON format of getting the frequency of each search, and providing a comprehensive histogram of each search.

### Messages
   #### **No or content of the user messages will be collected, analyzed, or stored. That's creepy. Only what type of message (text, photo, video etc.), sender, and time will be analyzed.**
Analysis of the messages revolves around the response time of each message.
 
This includes how fast each of you respond, the ability to keep a conversation going, if the relationship between you and the recipiant is one sided, who usually initiates the conversation, etc. This also includes the grouping of messages to find somewhat of conversations. 

- Response Times
- Amount of double messaging
- Most initiations of conversations
- Least self initiations conversations
    
    
## Technical
  All compilable code is written in python. Server is written with Flask/Flask-Cors and analysis utilizes NumPy, Pandas, and Scikit-learn.