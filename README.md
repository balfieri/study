This repository contains a Python3 script called run.py that will test you based on questions from a text file of your creation. It will randomly select questions and you must type the answers exactly (but upper/lower case is ignored). By default, it will give you 20 questions at a time, and it will re-test the questions that you missed. In test files like aviation.txt, the answers are too long, so one normally just looks at the answer and moves on without typing anything besides hitting ENTER.

There's another mode where you can tell it to simply print the question, pause, print the answer, pause, and then move on.  You don't have to click any buttons or type anything. Just say the answer in your head. Extra long answers will have additional delay added.  When it gets to the end of the questions, it currently just stops.  I am working on a way to have it speak the question and answer so you can quiz yourself while not looking at the screen (e.g., while driving). 

Each question in the file can be associated with one or more categories in {} separated by commas. In aviation.txt, the most important questions are also part of the "critical" category. Otherwise, categories include: reg, sys, perf, pilot, sop, weather, charts, etc. The program will prompt for the category you want to test.

There are a few text files provided for various topics of my interest. Feel free to use them or add your own:

    italian.txt
    french.txt
    aviation.txt                        -- private pilot checkride oral exam (includes categories)

Example of running the aviation questions:

    ./run.py aviation                   -- ask 20 questions at a time, prompt for answer
    ./run.py aviation 100               -- same, but 100 questions instead of default of 20
    ./run.py aviation 0                 -- same, but ALL questions instead of default of 20
    ./run.py aviation 0 4               -- same, but ALL questions and just print the question 
                                           and answer with 4-second delays

This is all open-source.  Refer to the LICENSE.md for licensing details.  

By the way, there is a roundabout way to run this on iOS. Use an app called Working Copy to clone this git repo, then use another app called PyTo to run the Python interpreter on iOS. You will need to enable Working Copy to be a Files "location" in order for PyTo to see the repo on your phone.  Once it's set up, you just need to "git pull" the repo occasionally. It's a pain to type answers on iOS, so this is a perfect place where you'll likely want it to just print the questions and answers with delays.

Bob Alfieri<br>
Chapel Hill, NC
