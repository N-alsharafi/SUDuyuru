############## contains all the preferences and settings for the project ##############



##########logging level###########

import logging
## Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_lvl = logging.INFO


######testing vs. production######

# Setting testing to True will run SUDuyuru in testing mode where it will send the emails
# to itself instead of the actual clients. 
# Potential problem: if the issue to be fixed is related to the clients themselves.

## Options: True, False
testing = False


#############scheduler############

# If scheduler is set to 1, SUDuyuru will run automatically between 9 and 10 am on mondays,
# wednesdays and fridays, script must be running for this to work
# If scheduler is set to 0, SUDuyuru will run manually when the script is executed, at the
# time of execution

## Options: 0, 1
scheduler = 0 



########################################################################################