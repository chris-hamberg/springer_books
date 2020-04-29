Downloads the free books from Springer onto your computer.

Their server is slow and some of these books are really huge.
If the scraper seems to be taking a long time, there is nothing
that I can do about this. It likely isn't stuck, but is busy downloading
the pdf. Please be patient. And you will likely want to allow this to run
over night. There are over 400 free books!


INSTRUCTIONS (for those not familiar with Python or git) :


1)  If you are a Windows user, you will need to download and install the latest 
    version of Python 3.8 on your computer.


2)  You also will need to download and install git on your computer.


3)  Once you have Python and git. In your command prompt (or terminal) 
    type the command:

    ```
    git clone https://github.com/chris-hamberg/springer_books.git
    ```

    This downloads the software that will get the books onto your machine.


4)  This step is OPTIONAL. If you are tech-savy, you may want to look up how to
    setup a Python virtual environment on your operating system. On Linux it is:

    ```
    python -m venv /home/user/environment_name && source /home/user/environment_name/bin/activate
    ```

5)  Now that you've cloned (downloaded) the software. cd into the clone directory
    and type:

    ```
    pip install -r requirements.txt
    ```

    This will install the Python dependencies into Python that are required for 
    the software to work.


6)  Now type (in the command prompt):

    ```
    python scraper.py
    ```

Your books are now downloading! The program will tell you in the terminal what 
it is doing. Getting all of the books takes a long time to finish, So go have a 
pizza, and watch a movie. It should be almost finished when you
come back!

The books will be in a directory called Books, inside of the springer_books 
directory.

If you did the OPTIONAL step 4, then you need to deactivate the virtual 
environment, and destroy it. On linux this is achived by the command:

    deactivate && rm -r /home/user/environment_name
    
