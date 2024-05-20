import requests
from pydal import DAL, Field

class CommunityManager:
    def __init__(self, db):
        self.db = db
        
    # Function to create the user table
    def create_community_table(self):
        self.db.define_table('communities', 
                            Field('community_name'),
                            Field('community_description'))
        self.db.commit()

    # Function to create a new community entry, if the community already exists, it will return an error
    def create_community(self, community_name, community_description): 
        # Before a new community is created, we need to check if the community already exists
        community = self.get_community_by_name(community_name)
        if community:
            return "Community already exists."
        else:
            self.db.communities.insert(community_name=community_name, community_description=community_description)

            self.db.commit()

            return "Community created successfully"
    
    # Function to remove a community
    def delete_community(self, communityname):
        # Check if the community exists
        community = self.get_community_by_name(communityname)
        if not community:
            return "Community does not exist."

        # Remove the community
        # self.db(self.db.communities.communityname == communityname).delete()

        # Remove the community record from the communities table
        self.db(self.db.communities.community_name == communityname).delete()

        print(f"Community removed successfully from the communities table. Deleting the {communityname} table....")

        # # Remove spaces from the community name
        # communityname = communityname.replace(" ", "")
        # self.db['users'].drop()

        self.db.commit()

        return "Community removed successfully"
    
    # Function to retrieve a list of all communities
    def get_communities(self):
        communities = self.db(self.db.communities).select()

        return communities

    # Function to retrieve a specific community by communityname
    def get_community_by_name(self, communityname):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        return community
    
    # Function to update a community by communityname, depending on the given fields
    def update_community(self, communityname, data):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        if community:
            if 'community_name' in data:
                community.update_record(community_name=data['community_name'])
            if 'community_description' in data:
                community.update_record(community_description=data['community_description'])

            self.db.commit()

            return "Community updated successfully"
        else:
            return "Community does not exist."
    