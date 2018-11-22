# dataviztry2

1. get urls
run scraper_final.py 
first need to run main() to get total pages of articles of the year you choose
Here you can make 'count' variable in get_years_available() plus 100 first in order to accelerate searching process, then plus 10 each time and at last make stepsize 1 to find the exact page number we have.

After you get the total page number, you can modify the number in the for loop in get_url()
Then comment main(), just run collect().
