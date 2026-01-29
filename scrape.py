# project: p3
# submitter: kasyoka
# partner: none
# hours: 25

import pandas as pd
from collections import deque 
import os 
from selenium.webdriver.common.by import By
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        
        # 1. clear out visited set and order list
        # 2. start recursive search by calling dfs_visit
        self.visited.clear()
        self.order.clear()
        self.dfs_visit(node) 

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        # 2. mark node as visited by adding it to the set
        # 3. call self.visit_and_get_children(node) to get the children
        # 4. in a loop, call dfs_visit on each of the children
        if node in self.visited:
            return
        self.visited.add(node)
        children = self.visit_and_get_children(node)
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self,node):
        # 1. Clear out visited set and order list
        # 2. Create a queue for BFS
        # 3. Loop to visit nodes until the queue is empty
        self.visited.clear()
        self.visited.add(node)
        queue = deque([node])
            # Dequeue a node from the front of the queue
            
            # If the node hasn't been visited yet
            # Mark the current node as visited
            # Get children of the current node
            # Enqueue all children of the current node
        while queue:
            current_node = queue.popleft()
            curr_node_children = self.visit_and_get_children(current_node)
            for child in curr_node_children:
                if child not in self.visited:
                    #print(child)
                    self.visited.add(child)
                    queue.append(child)

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for child,has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        return children

class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        
    def visit_and_get_children(self,file):
        children_list=[]
        file_path = os.path.join("file_nodes", file)
        with open(file_path, "r") as f:
            contents = list(f)
            values = contents[0].strip()
            self.order.append(values)
            file_children = contents[1].strip().split(",")
            children_list.append(file_children)
        return file_children
        
    def concat_order(self):
        return "".join(self.order)

# class WebSearcher(GraphSearcher):
#     def __init__(self,driver):
#         super().__init__()
#         self.driver = driver 
#         self.tables = []
#     def visit_and_get_children(self, url):
#         self.driver.get(url)
#         urls = []
#         links = self.driver.find_elements(By.TAG_NAME, "a")
#         for link in links:
#             href = link.get_attribute("href")
#             if href:
#                 urls.append(href)
#         self.order.extend(urls)
#         #extract table data from seleniums 
#         tables = self.driver.find_elements(By.TAG_NAME,"table")
#         for table in tables:
#             rows = table.find_elements(By.TAG_NAME,"tr")
#             table_data = []
#             for row in rows:
#                 columns = row.find_elements(By.TAG_NAME,"td")
#                 list = []
#                 for column in columns:
#                     list.append(column.text)
#                 table_data.append(list)
#             self.tables.append(table_data)    
#         return urls
#     def table(self):
#         dataframes=[]
#         for table in self.tables:
#             dataframes.append(pd.DataFrame(table))
#         return pd.concat(dataframes, ignore_index=True)
#     def table(self):
#     dataframes = []
#     headers = ["clue", "latitude", "longitude", "description"]
#     for table_data in self.tables:
#         dataframes.append(pd.DataFrame(table_data, columns=headers))
#     return pd.concat(dataframes, ignore_index=True)

    
import pandas as pd

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()  # Call the parent class constructor
        self.driver = driver
        self.fragments = []  # List to store table fragments

    def visit_and_get_children(self, url):
        self.driver.get(url)
        self.order.append(url)
        # print(url)
        urls = []
        # Extract all hyperlinks from the page
        links = self.driver.find_elements(by= 'tag name',value = 'a')
        for link in links:
            href = link.get_attribute("href")
            urls.append(href)
            
        # urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]
        
        # Use pandas to read table fragments and store them
        tables = pd.read_html(self.driver.page_source)
        self.fragments.extend(tables)
        
        return urls

    # def table(self):
        # Concatenate all table fragments
        # if self.tables:
        #     return pd.concat(self.tables, ignore_index=True)
    def table(self):
        # dataframes = []
        # headers = ["clue", "latitude", "longitude", "description"]
        # for table_data in self.tables:
        #     df = pd.DataFrame(table_data)
        #     if set(headers).issubset(df.columns):  # Check if the dataframe has the required columns
        #         dataframes.append(df[headers])  # Only select the required columns
        # if not dataframes:
        #     return pd.DataFrame()
        if self.fragments: 
            return pd.concat(self.fragments, ignore_index=True).dropna(axis = 1)
        else: 
            return None

    # Creating a password from the "clue" column
def reveal_secrets(driver, url, travellog):
    password = ''.join(travellog['clue'].astype(str))
    
    # for num in travellog["clue"].tolist():
    #     password = "".join(str(int(num)))
    # print(password)
    driver.get(url)

    password_input = driver.find_element(by='id', value='password-textbox')  
    password_input.send_keys(password)
    
    go_button = driver.find_element(by='id',value= 'submit-button')  
    go_button.click()
    
    time.sleep(2)
    
    view_location_button = driver.find_element(by='tag name',value='button')
    view_location_button.click()
    
    time.sleep(2)
    
    image_element = driver.find_element(by='id', value='image')
    image_url = image_element.get_attribute('src')
    response = requests.get(image_url).content
    
    with open('Current_Location.jpg', 'wb') as image_file:
        image_file.write(response)
    
    curr_location = driver.find_element(by='id',value ="location")
    # print(curr_location.text)
    return curr_location.text
    
        


