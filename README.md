This repository contains a Python3 script called run.py that will test you based on questions from a text file of your creation. It will randomly select questions and you must type the answers exactly (but upper/lower case is ignored). By default, it will give you 20 questions at a time, and it will re-test the questions that you missed.

There's another mode where you can tell it to simply print the question, pause, print the answer, pause, and then move on.  You don't have to click any buttons or type anything. Just say the answer in your head. Extra long answers will have additional delay added.  When it gets to the end of the questions, it currently just stops.  I am working on a way to have it speak the question and answer so you can quiz yourself while not looking at the screen (e.g., while driving).

There's a mechanism to only ask questions from part of the file.  This is often useful if you want to test yourself on more recent questions. Here's an example of how it works. If you tell the program "60 100", the program will only ask questions from the last 40% of the file.  If you tell it "10 40", it will ask questions only from 10% of the file in and 40% of the file in.  The default is obviously "0 100".

There are a few text files provided for various topics of my interest. Feel free to use them or add your own:

    italian.txt
    french.txt
    aviation.txt                        -- private pilot checkride oral exam

Example of running the aviation questions:

    ./run.py aviation
    ./run.py aviation 100               -- same, but 100 questions instead of default of 20
    ./run.py aviation 0                 -- same, but ALL questions instead of default of 20
    ./run.py aviation 0 3               -- same, but ALL questions and just print the question 
                                           and answer with 3-second delays
    ./run.py aviation 0 3 80 100        -- same as previous but only ask questions from the 
                                           last 20% of the file
    ./run.py aviation 0 3 0 100 1       -- questions that are acronyms (includes upper case letters, numbers, or spaces)
    ./run.py aviation 0 3 0 100 6       -- same as previous but acronyms must be at least 6 characters long

This is all open-source.  Refer to the LICENSE.md for licensing details.  

By the way, there is a roundabout way to run this on iOS. Use an app called Working Copy to clone this git repo, then use another app called PyTo to run the Python interpreter on iOS. You will need to enable Working Copy to be a Files "location" in order for PyTo to see the repo on your phone.  Once it's set up, you just need to "git pull" the repo occasionally. It's a pain to type answers on iOS, so this is a perfect place where you'll likely want it to just print the questions and answers with delays.

Bob Alfieri<br>
Chapel Hill, NC
