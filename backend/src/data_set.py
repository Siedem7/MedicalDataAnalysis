class data_set():
    """Class for data set. Contains data and informations about data set."""
    
    def __init__(self, name: str, description: str):
        """
        Constructor for data set. File contetnt is not loaded here.
        To load data use load_file_content method.
        
        Parameters:
            name (str): name of data set.
            description (str): description of data set.        
        """
        self.name = name 
        self.description = description
        self.file_content = None

    def load_file_content(self, file_path: str):
        """
        Load file content from file.
        
        Parameters:
            file_path (str): path to file with data set.
        """
        pass

    
    def prepare_statistics(self):
        """
        Used to prepare statistics based on data set.
        """
        pass


    def prepare_diagram(self, diagram_type: str):
        """
        Used to prepare diagram based on data set.
        """
        pass
