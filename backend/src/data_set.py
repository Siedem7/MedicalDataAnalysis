import pandas as pd

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
        self.data = None
        self.data_structure = None
        self.is_data_normalized = False

    def load_data(self, file_path: str):
        """
        Load file content from file.
        
        Parameters:
            file_path (str): path to file with data set.
        """
        self.is_data_normalized = False
        return pd.read_csv(file_path)

    
    def normalize_data(self, numerical_columns: list, categorical_columns: list, output_column: str):
        """
        Used to normalize data, based on provided infomrations about structure.

        Parameters:
            numerical_columns (list): list of names of numerical columns.
            categorical_columns (list): list of names of categorical columns.
            output_column (str): name of output column.
        """
        data_structure = dict()
        data_structure['categorical_columns'] = categorical_columns
        
        numercial_columns_list = list()
        for column in numerical_columns:
            numercial_columns_list.append({'name': column,'min': None, 'max': None, 'mean': None, 'median': None})

        data_structure['numerical_columns'] = numercial_columns_list
        data_structure['output_column'] = output_column

        self.data = pd.get_dummies(self.data, columns=data_structure['categorical_columns'])
        output_column = self.data.pop(data_structure['output_column'])
        self.data.insert(len(self.data.columns), output_column.name, output_column)

        for column in data_structure['numerical_columns']:
            column['min'] = self.data[column['name']].min()
            column['max'] = self.data[column['name']].max()
            column['mean'] = self.data[column['name']].mean()
            column['median'] = self.data[column['name']].median()
            self.data[column['name']] = (self.data[column['name']] - self.data[column['name']].min()) / (self.data[column['name']].max() - self.data[column['name']].min())

        self.is_data_normalized = True
    
    def get_data_structure(self):
        """
            Returns data structure with basic info about columns 
            (works only when data is normalized)
        """
        if (self.is_data_normalized):
            return self.data_structure
        else:
            return None
