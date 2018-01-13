# provide service name to check during execution

import sys
from gotrainalert_lib import AlertPage

go_page = AlertPage()
service_name = None

try:
    service_name = sys.argv[1]
except IndexError:
    print("Please provide a service name to check")
    exit(0)

print("Delay information for service {0}: \n    {1}".format(service_name, go_page.get_train_alert(service_name)))
