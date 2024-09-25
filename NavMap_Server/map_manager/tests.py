from django.test import TestCase

# Create your tests here.

#  get map without login
#  check out map without variation  ---> should just get map with that map_id
#  check out map with just map_name --> see if it gets all the variations

#   -----update-----
#  without login | with login
#  without permission | with permission
#  new variation | existing variation

#   -----create-----
#  without login | with login 
#  without permission | with permission   
#  map already exists with that name | map does not exist with that name


#   -----delete-----
#  without login | with login
#  without permission | with permission
#  last map variation | normal map variation | map does not exist | variation does not exist