import treelib

class AppStructure: 
    def __init__(self):
        self.structure = treelib.Tree()
        self.structure.create_node("Home", "/home", data={'url': "/home", 'no_display':False})
        self.default_app_id = '/home'
        
    def get_home(self):
        """
        Returns:
            [dict]: {"title": title of the "Home"-App, "url": "url"-tag of the "Home"-App}
        """
        title = self.structure.get_node(self.structure.root).tag
        link = self.structure.get_node(self.structure.root).identifier
        return {"title": title, "url": link}

    def set_home(self, title):
        """
        rename the "Home"-Node/App
        """
        self.structure.get_node(self.structure.root).tag = title


    # registers an app in the tree    
    def register_app(self, app, no_display=False):
        """
        This function registers an app in the tree relative to the specified parent node.

        Args:
            app ([DaisieApp]): [App to register]
            no_display (bool, optional): [determines, if the app is displayed in navigation components]. Defaults to False.
        """
        self.structure.create_node(app.title, app.id, parent=app.parent, data={'url':app.url, 'no_display':no_display})

    # registers an app in the tree
    # used for all apps in daisie_main
    def register_url(self, display, id, url, parent="/home", no_display=False):
        """[This does the same as register_app, but "manually". In most cases the other function should be used.]
        
        Args:
            display ([str]): [name to display]
            id ([str]): [id]
            url ([type]): [url-tag of the app]
            parent (str, optional): [id of the parent-node]. Defaults to "/home".
            no_display (bool, optional): [determines, if the app is displayed in navigation components]. Defaults to False.
        """
        self.structure.create_node(display, id, parent=parent, data={'url':url, 'no_display':no_display})

    def get_path(self, id):
        """[returns a list of url-snippets on a path from the root to a node]

        Args:
            id ([str]): [id of the app/node]

        Returns:
            [list]: [list of url-snippets on a path from the root to a node]
        """
        if id:
            nodes = [nid for nid in self.structure.rsearch(id)][::-1]
            #nodes.pop(0)
            res=[]
            for i, node in enumerate(nodes):
                res.append(self.structure.get_node(node).data['url'])
            return res
        else:
            return None

    # returns a list of nodes from the root to the node with id=id
    def nodes_from_root(self, id):
        """returns a list of nodes from the root to the node

        Args:
            id (str): id of the app

        Returns:
            list: node ids
        """
        if id:
            #id = self.structure.get_node(id)
            res = [self.structure.get_node(nid) for nid in self.structure.rsearch(id)][::-1]
            return res
        else:
            return None
    
    def get_parent_id(self, id):
        """returns the parent of the app

        Args:
            id (str): id of the app

        Returns:
            id (str): id of the parent of the app
        """
        return self.structure.parent(id).identifier
    
    # concatenates a list of url-snippets to a path
    def list_to_path(self, url_list):
        path = ""
        if url_list:
            url_list.pop(0)
            for x in url_list:
                path += x
            return path
        else:
            return None

    # returns the full url (not just the snippet) of given node
    def full_url(self, id):
        """returns the full url (not just the snippet) of given node

        Args:
            id (str): id of the app

        Returns:
            [str]: full url
        """
        return self.list_to_path(self.get_path(id))

    # returns a dictionary of apps on the path from root to the parent of the given node
    # keys: title of app
    # values: full url
    def get_dict_for_breadcrumbs(self, id):
        """returns a dictionary of apps on the path from root to the parent of the given node

        Args:
            id (str): id of the app

        Returns:
            [dict]: [keys: title of app, values: full url]
        """
        title = self.structure.get_node(id).tag
        id = self.get_parent_id( id)

        parents = self.nodes_from_root(id)
        parents.pop(0)
        dict = []
        default = self.structure.get_node(self.default_app_id)
        
        # if False: #self.default_app_id == id:
        #     print("default-app")
        #     dict.append({default.tag: None})
        # else:
        dict.append({self.structure.get_node(self.structure.root).tag: self.full_url(self.default_app_id)})
        for nid in parents:
            dict.append({nid.tag: self.full_url(nid.identifier)})
        dict.append({title:None})
        return dict

    def get_dict_for_navigation(self):
        navItemsList =[]
        pages = self.structure.children(self.structure.root)
        for chapter in pages:
            subpages = self.structure.children(chapter.identifier)
            if subpages:
                submenu = []
                for subchapter in subpages:
                    if subchapter:
                        if not subchapter.data['no_display']:
                            submenu.append({'link': self.full_url(subchapter.identifier), 'title': subchapter.tag})
            else:
                submenu = None
            if not chapter.data['no_display']:
                innerDict = {'link': self.full_url(chapter.identifier), 'title': chapter.tag, 'submenu': submenu}
                navItemsList.append(innerDict)
        return navItemsList

   
    def pages_with_links(self, node = None):
        if not node:
            node = self.structure.root
        # else:
        #     node = self.structure.get_node(node)
        dict = {}
        pages = self.structure.children(node)
        for chapter in pages:
            if chapter.data:
                dict.update({chapter.tag : None})
            else:
                if not chapter.data['no_display']:
                    dict.update({chapter.tag : self.full_url(chapter.identifier)})
        return dict      

    # returns a dictionary of all the children of the root
    # keys: title of app
    # values: id of app
    def get_pages(self):
        dict = {}
        pages = self.structure.children(self.structure.root)
        for chapter in pages:
            if chapter:
                if not chapter.data['no_display']:
                    dict.update({chapter.tag : chapter.identifier})
        return dict


    # returns a dictionary of all children of a given node
    # keys: title of app
    # values: full url
    def get_subpages(self, url):
        subpages = self.structure.children(url)
        innerDict = {}
        if subpages:
            for subchapter in subpages:
                if subchapter:
                    if not subchapter.data['no_display']:
                        innerDict.update({subchapter.tag : self.full_url(subchapter.identifier)})
        else:
            innerDict = {}
        return innerDict