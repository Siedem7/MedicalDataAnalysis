from src.data_set import data_set
import torch as torch
import torch.nn as nn 
import numpy as np

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
        self.data : data_set = None
        self.is_model_trained = False


    def set_structure(self, data, layers):
        """
        Load data for AI model.

        Parameters:
            training_data (data_set): training data.
            testing_data (data_set): testing data.
        """
        if not data.is_data_norm():
            raise RuntimeError("Data not normalized")

        self.data = data
        numpy_data = self.data.data.to_numpy(dtype=np.float32)
        
        model = nn.Sequential()
        model.append(nn.Linear(len(numpy_data[0])-1, layers[0]['output']))

        for layer in layers[1:]:
            match layer['function']:
                case "Linear":
                    model.append(nn.Linear(layer["input"], layer["output"]))
                case "ReLU":
                    model.append(nn.ReLU())
                case "Sigmoid":
                    model.append(nn.Sigmoid())
                case "Tanh":
                    model.append(nn.Tanh())

    

        self.model = model
        self.is_model_trained = False

    
    def create_model(self, training_procent: float, socketio):
        """
        Create model for AI model.

        Parameters:
            model (nn.Sequential): model to use.
        """
        training_points = int(len(self.data.data) * training_procent)
        numpy_data = self.data.data.to_numpy(dtype=np.float32)
        X_train = torch.from_numpy(numpy_data[:training_points, :-1])
        X_test = torch.from_numpy(numpy_data[training_points:, :-1])
        Y_train = torch.from_numpy(numpy_data[:training_points, -1])
        Y_test = torch.from_numpy(numpy_data[training_points:, -1])
        Y_train = torch.reshape(Y_train, (-1, 1))
        Y_test = torch.reshape(Y_test, (-1, 1))

        loss_fn = nn.BCELoss()
        optimizer = torch.optim.Adam(self.model.parameters())
        n_epochs = 100
        batch_size = 20
        for epoch in range(n_epochs):
            np.random.seed(epoch)  # Seed numpy with the epoch value
            torch.manual_seed(epoch)
            for i in range(0, len(X_train), batch_size):
                optimizer.zero_grad()
                X_batch = X_train[i:i+batch_size]
                outputs = self.model(X_batch)
                Y_batch = Y_train[i:i+batch_size]
                loss = loss_fn(outputs, Y_batch)
                loss.backward()
                optimizer.step()
            socketio.emit("model_training", f'Finished epoch {epoch}, latest loss {loss}')

        with torch.no_grad():
            Y_pred = self.model(X_test)

            # Convert predictions to 0 or 1 using rounding
            Y_pred_binary = torch.round(Y_pred)

            # Convert tensors to numpy arrays for comparison
            Y_pred_np = Y_pred_binary.numpy()
            Y_test_np = Y_test.numpy()

            # Calculate accuracy
            accuracy = np.mean(Y_pred_np == Y_test_np)
            socketio.emit("model_training", f"Accuracy: {accuracy}")

        self.is_model_trained = True


    def predict(self, data):
        """
        Predict data using model.

        Parameters:
            data (): data to predict.
        """
        if self.is_model_trained == False:
            raise Exception("Model is not trained")
        return self.model(data)

