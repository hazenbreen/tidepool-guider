Simple Python Script to help people looking to explore Tide Pools.

This script scrapes tide-forecast.com to find low tides that occur during daylight (after sunrise and before sunset) so that tide pools are optimally viewed. The time and height of the tide is returned to the user.

To run this script, assuming you have Python installed:
1) clone or download this repo
2) create a virtual environment
3) run "pip install" to install the following:
    - requests
    - BeautifulSoup
    - datetime
    - inquirer
4) run "python tidepool-guider.py"