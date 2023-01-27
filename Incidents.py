### DEVELOPED BY PAGERDUTY PROFESSIONAL SERVICES/SUCCESS ON DEMAND
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
### IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
### AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
### OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
### THE SOFTWARE.


from pdpyras import APISession
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import *

# declare the days that you want to go back asking for incidents
API_ACCESS_KEY = 'YOUR API KEY HERE'

# declare the days that you want to go back asking for incidents
days_to_get = 90  # X days back of data (max=180)

session = APISession(API_ACCESS_KEY)
list_incidents = pd.DataFrame()
offset = 0

today = datetime.today()
start_date = today - relativedelta(days=int(days_to_get - 1))

for x in range(days_to_get):
    offset = 0
    start = start_date + relativedelta(days=int(x))
    end = start_date + relativedelta(days=int(x + 1))
    response = session.get(
        "/incidents?since=" + str(start)[0:10] + "&until=" + str(end)[0:10] + "&limit=100&offset=" + str(offset))
    dataframe_incidents = pd.json_normalize(response.json()["incidents"], max_level=None)
    list_incidents = pd.concat([list_incidents, dataframe_incidents], ignore_index=True, axis=0)

    # this is going to fill the list_incidents dataframe with pagination

    while response.json()["more"]:  # more than 10.000 records in one day will fail
        limit = response.json()["limit"]
        offset = offset + int(limit)
        response = session.get(
            "/incidents?since=" + str(start)[0:10] + "&until=" + str(end)[0:10] + "&limit=100&offset=" + str(offset))
        dataframe_incidents = pd.json_normalize(response.json()["incidents"], max_level=None)
        list_incidents = pd.concat([list_incidents, dataframe_incidents], ignore_index=True, axis=0)

list_incidents.to_csv('logs.csv')
