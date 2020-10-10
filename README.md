This repository contains a Python3 script called run.py that will test you based on questions from a text file of your creation. It will randomly select questions and you must type the answers exactly (but upper/lower case is ignored). By default, it will give you 20 questions at a time.

It will re-test the questions that you missed.

There's another mode where you can tell it to simply print the question, pause, tell you the answer, pause, and then repeat.  
You don't have to click any buttons or type anything. Just say the answer in your head. Extra long answers will have additional delay added.
When it gets to the end of the questions, it currently just stops.
I am working on a way to have it speak the question and answer so you can quiz yourself while not looking at the screen such as while driving.

There are a few text files provided for various topics of my interest. Feel free to use them or add your own:

italian.txt<br>
french.txt<br>
aviation.txt - private pilot checkride oral exam<br>

Example of running the italian questions:

    ./run.py italian
    ./run.py italian 100                -- same, but 100 questions instead of default of 20
    ./run.py italian 0                  -- same, but ALL questions instead of default of 20
    ./run.py italian 0 3                -- same, but ALL questions and just print the question and answer with 3-second delays

This is all open-source.  Refer to the LICENSE.md for licensing details.  

By the way, there is a roundabout way to run this on iOS. Use an app called Working Copy to clone this git repo, then use another app called PyTo to run the Python interpreter on iOS. You will need to enable Working Copy to be a Files "location" in order for PyTo to see the repo on your phone.  Once it's set up, you just need to "git pull" the repo occasionally. It's a pain to type answers on iOS, so this is a perfect place where you'll likely want it to just print the question and answer rather
than prompting you.

Bob Alfieri<br>
Chapel Hill, NC
