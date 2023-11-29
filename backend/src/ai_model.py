from data_set import data_set
import torch as torch
import torch.nn as nn 

class AI_model():
    def __init__(self):
        self.name = "AI_Model"
        self.description = "This is a description of the AI_Model class"
        self.layers = []    
        self.model : nn.Sequential = None
        self.train_data : data_set = None
        self.test_data : data_set = None


    def load_data(self, training_data: data_set, testing_data: data_set):
        self.train_data = training_data
        self.test_data = testing_data

    
    def create_model(self, model: nn.Sequential):
        self.model = model


    def predict(self, data):
        return self.model.eval(data)

