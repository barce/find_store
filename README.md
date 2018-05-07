# find_store

# Note on this implementation

This code finds the closest store location to an address using 
googlemaps, and a kd-tree. A kd-tree is a kind of binary space
partitioning tree that is useful for nearest neighbor searches.

How to install:

Be sure to use Python 3.5

export GROVECO_GOOGLE_API_KEY="YOUR_API_KEY_FOR_GOOGLE_HERE"
pip install googlemaps

How to test:
python mtests.py

How to run:
./find_store --address="600 California Street, San Francisco, CA 94108"



