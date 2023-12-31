## changes

### cli.py

* When filtering the images you choose to import the filterfunctions manually from python_filters.py .ect. This is fine, however there's already a function, get_filter(filter, implementation),
in __init__.py that does this for us. So I used this instead.
* Similarly to the previous point the io.py file has a function, read_image(filename), for opening an image as an array. It's really not important, so I didn't bother changing it in other files.
* In the run_filter function you didn't do anything with the scale argument. So I added this functionality. 
* When you added the output filename and file arguments you specified the number of args to be one (nargs = 1). This nested the arguments in a list. So in the run_filteryou had to index the first element.
This is a bit nitpicky, but decided to change this. 

### timing.py
* Added the calls argument in make_reports when calling on time_one, in order to make reports with different nr. of calls.
* Also implemented the get_filter function.

## Test Functions

It wasn't made very clear in the task, but the image, refrence_gray and reference_sepia arguments are defined in the conftest.py file. These are global variables defined when you run pytest. Image is an image array with random rbg values and refrence_gray and refrence_sepia are filtered versions of this random image, using your python implementation. Knowing this you only need to rigorusly test random pixles in the python implementaton, and then compare the numpy and numba implementations to the refrences.  
Note: The image global variable was set to default_image().copy not random_image().copy. I'm thing it's supposed to be random so I changed it.


### test_python.py
* asserted uniform values for all r, g, b values insted of just a couple.

### test_numpy.py
* checked that the refrence and the numpy filtered version were close enough.
* Removed the verifying of individual pixels as this is redundant after already asserting similarity with the python filtered version.

