# 389LFinal

Final project for CMSC389L Spring 2018

Overview:
I made a chatbot that can talk to users about medication and give information about the pros and cons of them. It can also briefly engage the users in conversation about how they are feeling and direct them to appropriate resources if they need it. To do this, I used Amazon Lex, Lambda, and S3 to make the bot and store the necessary information, and Twilio as a way for the users to interact with the bot. This version is a prototype with limited capability, but it could easily expand to cover far more medications and emotions. It could also have more complicated interaction with users through further work in Amazon Lex and Lambda.

Step 1: Creating the HealthBot

First, I created a custom bot in Amazon Lex.  I gave it two intents: IWantToTalk and Medication to represent the two topics the HealthBot will talk about with the User.

IWantToTalk is used when the user wants to talk to the bot about how they are feeling. First, I put in some sample utterances such as Hi, I need to talk to someone and I want to talk.  Then I added created a slot type called Emotions to read in responses from the user.  Permissible values are good, bad, anxious, and depressed. As this bot scales, I could add more options to deal with more issues. I then created a slot titled Feeling using the Emotion slot type with the prompt "How are you feeling".

Medication is used when the user wants to ask about medication. The smaple utterances for this are "I have a question about medication" and "I want to compare meds."  I created a slot type called medication which accepts Prozac, Wellbutrin, and Zoloft as values.  Many more can be put in here, but for this project, I decided to just put in these three as they are commonly used to treat depression and anxiety. I then created another slot that asks the user if they want to compare this medication to others, or if they would just like information on this medication.

I then built the lambda functions corresponding to these intents based off of the Amazon lex examples avaliable online. The code is in the lambda.py file.

Step 2: Putting the data into s3 buckets

I found the necessary information about the different types of medication online (from iodine.com), and put the data in s3 buckets. I then wrote the lambda code that accesses the buckets when they are needed.

Step 3: Integrating the chatbot with Twilio

Finally, I integrated the chatbot into twilio to allow users to actually interact with it through text. To do so, I went to the channels tab of the HealthBot in the AWS GUI, made a twilio account and put in the appropriate information. Then I enabled the twilio project and associated a phone number with the HealthBot.

Architecture Diagram:
See architecure diagram file for picture

Demo Video:
https://youtu.be/k2JUd9lL0Kw
