"""Adaptor class to map the fields from GitHub user data to FreshDesk contact""" 

class DataAdaptor:
    def __init__(self,mappings):
        """Adaptor initialization based on the dictionary mapping dictionary: 
            { GITHUB_field : FreshDesk_field }
        """
        self.github_to_freshdesk = mappings
        self.freshdesk_to_github = {v: k for k, v in self.github_to_freshdesk.items()} 

    def covert_github_to_freshdesk(self,github_data):
        """Adapting data from GH to FD"""
        newdata = {}
        for k,v in github_data.items():
            if k in self.github_to_freshdesk.keys():
                newdata[self.github_to_freshdesk[k]] = v
        if not newdata['name']:
            newdata['name'] = github_data['login']
            print('Github name was None. Used login id instead')
        if 'description' not in newdata.keys() or not newdata['description']:
            newdata['description'] = "Transfer from GitHub"
        return newdata



