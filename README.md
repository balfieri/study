This repository contains a Python3 script called run.py that will test you based on questions from a text file of your creation. It will randomly select questions and you must type the answers exactly (but upper/lower case is ignored). By default, it will give you 20 questions at a time, and it will re-test the questions that you missed. 

There's another mode (which I normally use) where you can tell it to simply print the question, pause, print the answer, pause, and then move on.  You don't have to click any buttons or type anything. Just say the answer in your head. Extra long answers will have additional delay added. When it gets to the end of the questions, it will restart the process. The -q 0 options says to use all questions. 
The -ps <sec> option specifies the pause time in seconds.

Multiple subjects can be given on the command line, separated by commas with no spaces. For example "run.py aviation,aviation_ifr" will cause it to read in all questions from aviation.txt and aviation_ifr.txt.

Each question in the file can be associated with one or more categories in {} separated by commas. In aviation.txt, the most important questions are also part of the "critical" category. Otherwise, categories include: reg, sys, perf, pilot, sop, weather, weathersymbol, chart. Use the -cat command-line option to specify the categories, separated by commas.

Answers in the file will be split along semicolons onto separate lines. The answer must currently be all on one line in the file, so this allows a more pleasant output. [I might change that to just allow multi-line answers in the file as there is already a blank line between questions.]

There are a few text files provided for various topics of my interest. Feel free to use them or add your own:

    aviation.txt                        -- private pilot checkride oral exam (includes categories)
    aviation_ifr.txt                    -- instrument pilot checkride oral exam
    italian_basic.txt                   -- basic and a few intermediate words
    italian_advanced.txt                -- higher-intermediate to advanced words
    italian_expressions.txt             -- expressions that have existed for a while
    italian_slang.txt                   -- more modern slang
    italian_vulgar.txt                  -- vulgar phrases (parolacce)
    french.txt                          -- my daughter's old word list 

Example of running the aviation questions:

    ./run.py aviation                   -- ask 20 questions at a time, prompt for answer
    ./run.py aviation -q 100            -- same, but 100 questions instead of default of 20
    ./run.py aviation -q 0              -- same, but ALL questions instead of default of 20
    ./run.py aviation -q 0 -ps 4        -- same, but just print answer with 4-second pause
    ./run.py aviation -q 0 -ps 4 -cat critical -- same but only questions in the 'critical' category
    ./run.py aviation,aviation_ifr -q 0 -ps 4 -cat critical -- same, using both aviation.txt and aviation_ifr.txt

This is all open-source. Refer to the LICENSE.md for licensing details.  

By the way, there is a roundabout way to run this on iOS. Use an app called Working Copy to clone this git repo, then use another app called PyTo to run the Python interpreter on iOS. You will need to enable Working Copy to be a Files "location" in order for PyTo to see the repo on your phone. Once it's set up, you just need to "git pull" the repo occasionally. Kind of clunky, but useful.

For aviation.txt, I need to add a way to narrow down the aircraft type for which questions can be asked. Currently, I include questions about both 172SP and PA-28-161, which are the two planes I currently fly.

Bob Alfieri<br>
Chapel Hill, NC
