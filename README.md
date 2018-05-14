# 389LFinal

Final project for CMSC389L Spring 2018

Step 1: Creating the HealthBot

First, I created a custom bot in Amazon Lex.  I gave it two intents: IWantToTalk and Medication to represent the two topics the HealthBot will talk about with the User.

IWantToTalk is used when the user wants to talk to the bot about how they are feeling. First, I put in some sample utterances such as Hi, I need to talk to someone and I want to talk.  Then I added created a slot type called Emotions to read in responses from the user.  Permissible values are good, bad, anxious, and depressed. As this bot scales, I could add more options to deal with more issues. I then created a slot titled Feeling using the Emotion slot type with the prompt "How are you feeling".

Medication is used when the user wants to ask about medication. The smaple utterances for this are "I have a question about medication" and "I want to compare meds."  I created a slot type called medication which accepts Prozac, Wellbutrin, and Zoloft as values.  Many more can be put in here, but for this project, I decided to just put in these three as they are commonly used to treat depression and anxiety. I then created another slot that asks the user if they want to compare this medication to others, or if they would just like information on this medication.

I then built the lambda functions corresponding to these intents based off of the Amazon lex examples avaliable online. The code is in the lambda.py file.

Finally, I found the nessecary information about the different types of medication online (from iodine.com), put the data in s3 buckets, and wrote the lambda code that accesses the buckets when they are needed.
