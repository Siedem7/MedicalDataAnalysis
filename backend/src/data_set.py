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

    def is_data_norm(self):
        return self.is_data_normalized

    def load_data(self, file_path: str):
        """
        Load file content from file.
        
        Parameters:
            file_path (str): path to file with data set.
        """
        self.is_data_normalized = False
        na_values = ['NA', 'N/A', 'missing', '']
        self.data = pd.read_csv(file_path, na_values=na_values)
        print(self.data)
        self.data = self.data.fillna(self.data.mean())
        print(self.data)

    
    def normalize_data(self, numerical_columns: list, categorical_columns: list, output_column: str):
        """
        Used to normalize data, based on provided infomrations about structure.

        Parameters:
            numerical_columns (list): list of names of numerical columns.
            categorical_columns (list): list of names of categorical columns.
            output_column (str): name of output column.
        """
        data_structure = dict()

        numerical_columns_list = list()
        for column in numerical_columns:
            numerical_columns_list.append({'name': column,'min': None, 'max': None, 'mean': None, 'median': None})


        data_structure['numerical_columns'] = numerical_columns_list
        data_structure['categorical_columns'] = list()
        data_structure['output_column'] = output_column

        #original_columns = self.data.columns.tolist()

        for column  in categorical_columns:
            column_values = list(set(self.data[column].tolist()))
            data_structure['categorical_columns'].append({'name': column, 'values': column_values})

    
        self.data = pd.get_dummies(self.data, columns=categorical_columns)
        output_column = self.data.pop(data_structure['output_column'])
        self.data.insert(len(self.data.columns), output_column.name, output_column)

        #data_structure['categorical_columns'] = [col for col in self.data.columns.tolist() if col not in original_columns]

        for column in data_structure['numerical_columns']:
            column['min'] = float(self.data[column['name']].min())
            column['max'] = float(self.data[column['name']].max())
            column['mean'] = float(self.data[column['name']].mean())
            column['median'] = float(self.data[column['name']].median())
            self.data[column['name']] = (self.data[column['name']] - self.data[column['name']].min()) / (self.data[column['name']].max() - self.data[column['name']].min())

        self.data = self.data.sort_index(axis=1)
        self.data_structure = data_structure
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
