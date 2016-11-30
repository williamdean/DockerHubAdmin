#!/usr/bin/env python3

import http.cookiejar
import urllib.request
import urllib.parse
import json

class DockerHubAdmin(object):

    def __init__(self, username, password):
        self.apiURL =  "https://hub.docker.com/v2/"
        #javascript web token
        self.jwt = self._login(username, password)

    def _login(self, username, password):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
        values = {'password': password, 'username': username}
        data = json.dumps(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.apiURL + 'users/login/', data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib.request.urlopen(req)
        data = resp.read()
        data = json.loads(data.decode("utf8"))
        jwt = "Bearer " + data['token']
        return jwt

    def _request(self, params, data, method):
        if data:
            data = json.dumps(data)
            data = data.encode('utf-8')
            req = urllib.request.Request(self.apiURL + params, data)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib.request.Request(self.apiURL + params)
        req.add_header('Authorization', self.jwt)
        if method: req.method = 'DELETE'
        resp = urllib.request.urlopen(req)
        resp = resp.read().decode("utf8")
        #Handle empty error free response
        if not resp: return True
        data = json.loads(resp)
        #Some API calls force pagination
        if 'next' in data:
            if data['next']:
                #Next page
                page = data['next'].replace(self.apiURL, '')
                results = data['results'] + self._request(page, None, None)
            else:
                #Last page
                return data['results']
        else:
            #No pagination
            return data

        return results

    def listMembers(self, organization, group):
        #Groups belong to an org
        members = []
        params = 'orgs/' + organization + '/groups/' + group + '/members/'
        data = self._request(params, None, None)
        for u in data: members.append(u['username'])
        return members

    def listGroups(self, organization):
        params = 'orgs/' + organization + '/groups/'
        data = self._request(params, None, None)
        groups = []
        for group in data:
            groups.append(group['name'])
        return groups

    def findUserGroups(self, organization, user):
        user_groups = []
        all_groups = self.listGroups(organization)
        for group in all_groups:
            if user in self.listMembers(organization, group):
                user_groups.append(group)
        return user_groups

    def addUserGroup(self, organization, user, group):
        params = 'orgs/' + organization + '/groups/' + group + '/members/'
        data = {'member': user}
        self._request(params, data, None)
        #need to check return status to make sure user is added
        return True
        
    def removeUserGroup(self, organization, user, group):
        params = 'orgs/' + organization + '/groups/' + group + '/members/' + user + '/'
        self._request(params, None, 'DELETE')
        #need to check return status to make sure user is deleted 
        return True
