#!/usr/bin/env python3

import DockerHubAdmin
import argparse

parser = argparse.ArgumentParser(description='Python admin interface to Docker Hub')
parser.add_argument('-u','--username', help='Admin username for Docker Hub', required=True)
parser.add_argument('-p','--password', help='Admin password for Docker Hub', required=True)
parser.add_argument('-o','--organization', help='Password for Docker Hub', required=True)
parser.add_argument('--user', help='Non-Admin User Account on Docker Hub')
parser.add_argument('-t','--team', help='A Docker Hub Team')
parser.add_argument('--adduser', help='Add account to a Docker Hub Team', action='store_true')
parser.add_argument('--rmuser', help='Remove account from a Docker Hub Team', action='store_true')
parser.add_argument('--listmembers', help='List members of a Docker Hub Team', action='store_true')
parser.add_argument('--listteams', help='List all teams within an org', action='store_true')
parser.add_argument('--finduserteams', help='List all teams an account is a member of within an org', action='store_true')
args = parser.parse_args()

hub = DockerHubAdmin.DockerHubAdmin(args.username, args.password)

if args.listteams:
    print(hub.listGroups(args.organization))
elif args.listmembers:
    print(hub.listMembers(args.organization, args.team))
elif args.finduserteams:
    print(hub.findUserGroups(args.organization, args.user))
elif args.adduser:
    hub.addUserGroup(args.organization, args.user, args.team)
elif args.rmuser:
    hub.removeUserGroup(args.organization, args.user, args.team)