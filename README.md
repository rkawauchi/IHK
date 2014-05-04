IHK
===

Indian Health Kiosk

==

HOW TO MAKE STUFF WORK

1. Update the database. To do that, delete the database.sqlite3 file. Then run the following:


        python main.py -i
   

That tells the program to automatically recreate the database.

2. Choose a state and district that actually has an Aravind hospital in real life. Let's say you choose the Theni district, in the Tamil Nadu state.

3. Run the following to test the program:
        

        python main.py --test-state "Tamil Nadu" --test-district Theni --pop-gen-limit-dist 10000


   *Option 1: To run the test multiple times, att "-t n" where n = number of trials:* 

        
        python main.py --test-state "Tamil Nadu" --test-district Theni --pop-gen-limit-dist 10000 **-t 1000**


   *Option: If you want to run the full test (this will take about 8 min):*
        

        python main.py --test-state "Tamil Nadu" --test-district Theni


The first time, the program will add the population of Theni to the database, using people.py. That will take a few minutes. After that is done, it will test the population using the solution in health.py and the filtering in util.py.

4. Adjust parameters so you understand how stuff works.

5. Add more detail so the simulation becomes remotely accurate!
