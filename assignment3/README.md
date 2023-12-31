# Instapy
## What does it do? 
Instapy is a portmanteau of instagram and python, and as you might guess, is an
epic package for filtering your instagram photos.  It has two filters sepia
(vintage swag) and gray (oldy, like a grandpa). These filters can be applied
using three different implementations python (slow), numpy (fast) and numba
(faster).
## How to install it
**step 1:** 

Clone the repository.
- SSH: `git clone git@github.uio.no:IN3110/IN3110-dtsteene.git`
- HTTPS: `git clone https://github.uio.no/IN3110/IN3110-dtsteene.git`

**step 2:**

Change working directory to `instapy/assignment3` and run the command:
```
pip install .
```
This will install all pip installable packages in this directory.
Now you should be able to use the package as intended. :tada:

## How to use the package
Filter an image of your choosing by running the following command:
```
instapy some_directory/my_image.jpg <args>
```
To see which args you can pass with your image type

```
instapy -h
```
