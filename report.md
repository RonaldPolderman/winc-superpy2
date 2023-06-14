SuperPy Report.

The 4th commit for another very challenging assigment, I had a hard time understanding what exactly was asked in the assignment and then figuring out how the required modules like date, argparse and csv files worked.
After a lot of Google reading and going through all the docs at docs.python i had a minor grasp of understanding what to do.

Added the report.md this time since i did not add one in the 1st commit.
Added comments.
Added a dynamic date instead of a hardcoded date to the current_date.txt
Fixed a small bug in advancing time. It always printed "Please enter a valid number of days, example: 3".
Fixed another bug in advance date. Changed the writing of current date to the current_date.txt inside the def_buy_product so it only writes the date once instead of looping over it every time you advance time.
Fixed an issue when buying a product after advancing time it still had the date today instead of the advanced time.
Added a --setdate function as requested (even though i don't really see that in the exersize as suggested the way i read it it says write the date of today and advance from there which is way more logic in the light of this exersize in my opinion)
Added csv files for inventory, revenue, profit and expired products so that the data requested is not only printed in the terminal but also written on a csv file.

Here are the 3 notable elements.

    1. The expired products are handled at the same time the date is advanced. This keeps the code clean in my opinion and you get a notification in the command line so you know that a product expired. The expired products can obviously also be looked up with the --expired command in the CLI. They are put in the sold file without profit so it doesn't polute the revenue - profit stats and chart.

    2. I used 'try' and 'except' statements to distinguish between different types of dates. For example, I used this in the function for calculating revenue for a particular day or month. By attempting to execute the code when a day is entered, it will only run if it is a day. If a month is entered, it will raise a ValueError and then attempt to run the code for a month. If that also raises a ValueError, then the user has entered neither a day nor a month, and the function will return an error.

    3. I used a separate function for returning a table. This function is not called directly in the main program but is instead used when another function requires a table to be returned.

I am pretty sure the code can be a lot cleaner by putting repeating parts of code into a seperate function but since I am a tad timepressed and that would take me a lot of time I am leaving it at this.
Like i said before I am encountering lots of problems to understand what is asked in general, not only in this assignment but in all / most assignments, and translating that to code is even a bigger challenge. As a starting, or actually before even starting, programmer trying to find the solution in a world of data, explainations, opinions and text does not come easy to me.

That being said, once I do manage to finish an assigment it's a fulfilling feeling.
