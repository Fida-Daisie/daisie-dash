import treelib

class AppStructure: 
    def __init__(self):
        self.structure = treelib.Tree()
        # self.structure.create_node("root", "/root", data={'url': "/root", 'no_display':False})
        self.register_url(display="root", id="root", url="/root", parent=None)
        self.default_app_id = 'root'
        self._apps = {}
        
    def get_root(self):
        """
        Returns:
            [dict]: {"title": title of the "root"-App, "url": "url"-tag of the "root"-App}
        """
        title = self.structure.get_node(self.structure.root).tag
        link = self.structure.get_node(self.structure.root).identifier
        return {"title": title, "url": link}

    def set_root_name(self, title):
        """
        rename the "root"-Node/App
        """
        self.structure.get_node(self.structure.root).tag = title


    # registers an app automatically in the tree
    # used for all apps in daisie_main
    def register_app(self, app, default_app=False, no_display=False, no_sitemap=False):
        """
        This function registers an app in the tree relative to the specified parent node.

        Args:
            app ([DaisieApp]): [App to register]
            default_app (bool, optional): [determines, whether the app is the default app]. Defaults to False.
            no_display (bool, optional): [determines, if the app is displayed in navigation components]. Defaults to False.
            no_sitemap (bool, optional): [determines, if the app appears in the sitemap]. Defaults to False.
        """
        self.register_url(app.title, app.id, app.url, app=app, parent=app.parent, default_app=default_app, no_display=no_display, no_sitemap=no_sitemap)

    # registers an app manually in the tree
    def register_url(self, display, id, url, app=None, parent="root", default_app=False, no_display=False, no_sitemap=True):
        """[This does the same as register_app, but "manually". In most cases the other function should be used.]
        
        Args:
            display ([str]): [name to display]
            id ([str]): [id]
            url ([type]): [url-tag of the app]
            app ([DaisieApp | None]): [app-tag of the app, holds the app instance] Defaults to None.
            parent (str, optional): [id of the parent-node]. Defaults to "root".
            default_app (bool, optional): [determines, whether the app is the default app]. Defaults to False.
            no_display (bool, optional): [determines, if the app is displayed in navigation components]. Defaults to False.
            no_sitemap (bool, optional): [determines, if the app appears in the sitemap]. Defaults to True
        """
        self.structure.create_node(tag=display, identifier=id, parent=parent, data={'url':url, 'no_display':no_display, "no_sitemap":no_sitemap, "app": app, "default_app": default_app})
        if app:
            self._apps.update({self.full_url(id): app})

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
    
    def list_to_path(self, url_list):
        """Concatenates a list of url-snippets to a path.
        """
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
    
    def get_urls_for_sitemap(self):
        return [self.full_url(node.identifier) for node in self.structure.all_nodes() if not node.data["no_sitemap"]]
   
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
    def get_pages(self, id="root"):
        dict = {}
        pages = self.structure.children(id)
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

    def get_apps(self):
        """returns dict with full URL as keys and the app instances as values"""
        return self._apps