import os
from app import app
from flask_frozen import Freezer

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    freezer = Freezer(app)
    freezer.freeze()
