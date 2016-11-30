# DockerHubAdmin
Python 3 interface to Docker Hub admin functions.

##Example: Getting a list of teams for an organization:
>>>./example.py  -u mydockerusername -p mydockerpassword -o myorg --listteams

##Example: Listing all members of a team:
>>>./example.py  -u mydockerusername -p mydockerpassword -o myorg -t myteam --listmembers

##Example: Getting a list of all teams a user belongs to:
>>>./example.py  -u mydockerusername -p mydockerpassword -o myorg --user the_user --finduserteams

##Example: Adding a user to a team:
>>>./example.py  -u mydockerusername -p mydockerpassword -o myorg --user the_user --adduser -t myteam

##Example: Removing a user from a team:
>>>./example.py  -u mydockerusername -p mydockerpassword -o myorg --user the_user --rmuser -t myteam
