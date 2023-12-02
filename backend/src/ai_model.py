from data_set import data_set
import torch as torch
import torch.nn as nn 

class AI_model():
    """
    Class for AI model. Contains model and informations about model.
    """

    def __init__(self, name: str, description: str):
        """
        Constructor for AI model. Model is not created here.
        Initialize model with create_model method.

        Parameters:
            name (str): name of AI model.
            description (str): description of AI model.
        """
        self.name = name
        self.description = description
        self.layers = []    
        self.model : nn.Sequential = None
        self.train_data : data_set = None
        self.test_data : data_set = None


    def load_data(self, training_data: data_set, testing_data: data_set):
        """
        Load data for AI model.

        Parameters:
            training_data (data_set): training data.
            testing_data (data_set): testing data.
        """
        self.train_data = training_data
        self.test_data = testing_data

    
    def create_model(self, model: nn.Sequential):
        """
        Create model for AI model.

        Parameters:
            model (nn.Sequential): model to use.
        """
        self.model = model


    def predict(self, data):
        """
        Predict data using model.

        Parameters:
            data (): data to predict.
        """
 
        return self.model(data)

