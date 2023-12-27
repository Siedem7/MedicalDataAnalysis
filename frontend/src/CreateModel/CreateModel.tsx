import React, { useState, useEffect } from "react";
import { getAvailableDatasets, logout, DataSet } from "../Utils/ApiUtils";
import { Link } from "react-router-dom";
import NewLayer from "./NewLayer";

import "./CreateModel.css";

/**
 * Represents an interface for a layer.
 * @interface
 */
export interface Layer {
  /**
   * Function type of the layer. One of Linear, Sigmoid, Tanh, ReLU
   * @type {string}
   */
  function: string;

  /**
   * Input value of the layer.
   * @type {number|null}
   */
  input: number | null;

  /**
   * Output value of the layer.
   * @type {number|null}
   */
  output: number | null;
}

/**
 * React component responsible for creating AI model based.
 * @component
 * @returns {JSX.Element} Rendered JSX element.
 */
export default function CreateModel() {
  // Retrieve the user token from local storage
  let token = localStorage.getItem("token") as string;

  const [numericalColumns, setNumericalColumns] = useState<Array<String>>()
  const [categoricalColumns, setCategoricalColumns] = useState<Array<String>>()
  const [outputColumn, setOutputColumn] = useState<String>()

  const [batchSize, setBatchSize] = useState(50);
  const [epochsAmount, setEpochsAmount] = useState(50);
  const [trainingPercent, setTrainingPercent] = useState(90);
  const [description, setDescription] = useState("");
  const [modelName, setModelName] = useState("");

  const [layers, setLayers] = useState<Array<Layer>>([]);

  const [firstLayerOutput, setFirstLayerOutput] = useState(10);
  const [datasets, setDatasets] = useState<Array<DataSet>>([]);
  const [selectedDataset, setSelectedDataset] = useState<DataSet>();
  const [isSelectedDataset, setIsSelectedDataset] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const openPopup = () => {
    let inputSize = 0;
    if (layers.length === 0) {
      inputSize = firstLayerOutput;
    } else {
      for (var i = layers.length - 1; i >= 0; i--) {
        if (layers[i].output !== null) {
          inputSize = layers[i].output!;
          break;
        }
      }
      inputSize = inputSize === 0 ? firstLayerOutput : inputSize;
    }

    return (
      <NewLayer
        setOpenPopup={setIsPopupOpen}
        layers={layers}
        setLayers={setLayers}
        inputSize={inputSize}
      />
    );
  };

  const createModel = () => {
    if (!checkModel()) {
      return 
    }
    console.log(numericalColumns)
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", "Bearer " + token);
    
    var raw = JSON.stringify({
      "file_id": selectedDataset?.file_id,
      "model_name": modelName,
      "model_desc": description,
      "training_percent": trainingPercent / 100.0,
      "numerical_columns": numericalColumns,
      "categorical_columns": categoricalColumns,
      "output_column": outputColumn,
      "layers": Array<any>().concat([{"output": firstLayerOutput}]).concat(layers).concat({"function": "Sigmoid"}),
      "epochs": epochsAmount,
      "batch_size": batchSize
    });
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw
    };
    
    fetch("http://127.0.0.1:5000/create_model", {...requestOptions, redirect: 'follow'})
      .then(response => response.text())
      .then(result => console.log(result))
      .catch(error => console.log('error', error));
  }

  const checkModel = ():boolean => {
    if (modelName === "" || description === "") {
      alert("Model require name and description.")
      return false
    }
    if (layers.length !== 0) {
      let outputSize = 0;
      for (var i = layers.length - 1; i >= 0; i--) {
        if (layers[i].output !== null) {
          outputSize = layers[i].output!;
          break;
        }
      }

      if (outputSize === 1 || (outputSize === 0 && firstLayerOutput === 1)) {
        alert("Model is valid. You may continue.")
        return true
      }
      else {
        alert("Your model is invalid.")
        return false
      }
    }
    else if (layers.length === 0 && firstLayerOutput === 1 ) {
      alert("Your model is valid. You may continue")
      return true
    }
    else {
      alert("Your model is invalid.")
      return false
    }
  };

  useEffect(() => {
    getAvailableDatasets(token, setDatasets);
  }, []);

  return (
    <>
      <div className="header">
        <h1>Create Model</h1>
        <button onClick={logout}>log out</button>
      </div>
      {isSelectedDataset ? (
        <div>
          <div className="model-config">
            <div className="column left-column">
              <input 
              type="text" 
              id="model-name" 
              name="model-name" 
              onChange={(event) => {
                setModelName(event.target.value)
              }}
              placeholder="Insert model name here."
              />
              <textarea
                name="description"
                id="description"
                cols={30}
                rows={5}
                onChange={(event) => {
                  setDescription(event.target.value)
                }}
                placeholder="Insert description here."
              ></textarea>
            </div>

              <div className="layer-container column">
                <div className="layer input-layer">
                  <label htmlFor="first-layer-input">Output: </label>
                  <input
                    type="number"
                    name="first-layer-input"
                    id="first-layer-input"
                    onChange={(event) =>
                      setFirstLayerOutput(Number.parseInt(event.target.value))
                    }
                    value={firstLayerOutput}
                    disabled = { layers.length > 0 }
                  />
                </div>

                {layers.map((layer: Layer) => (
                  <div className="layer" key={layer.function}>
                    {layer.input === null ? (
                      layer.function
                    ) : (
                      <>
                        {layer.function} Input: {layer.input} Output:{" "}
                        {layer.output}
                      </>
                    )}
                  </div>
                ))}

                <div className="layer output-layer">Sigmoid</div>
              </div>
            <div className="column right-column">
              <div>
                <label htmlFor="batch-size">Insert batch size: </label>
                <input
                  type="number"
                  name="batch-size"
                  id="batch-size"
                  onChange={(text) => {
                    setBatchSize(Number.parseInt(text.target.value));
                  }}
                  min={1}
                  value={batchSize}
                />
              </div>
              <div>
                <label htmlFor="epochs-number">Insert number of epochs: </label>
                <input
                  type="number"
                  name="epochs-number"
                  id="epochs-number"
                  onChange={(text) => {
                    setEpochsAmount(Number.parseInt(text.target.value));
                  }}
                  min={1}
                  value={epochsAmount}
                />
              </div>
              <div>
                <label htmlFor="training-percent">
                  Insert training percent:{" "}
                </label>
                <input
                  type="number"
                  name="training-percent"
                  id="training-percent"
                  onChange={(text) => {
                    setTrainingPercent(Number.parseInt(text.target.value));
                  }}
                  min={1}
                  max={99}
                  value={trainingPercent}
                />
              </div>
            </div>
          </div>

          <div className="create-model-buttons-container">
            <div className="change-dataset-button"> 
              <button
                onClick={() => {
                  setIsSelectedDataset(false);
                }}
              >
                Change Dataset
              </button>
            </div>

            <div className="layer-manipulation-buttons">
              <button
                onClick={() => {
                  const updatedLayers = [...layers]
                  updatedLayers.pop()
                  setLayers(updatedLayers)
                }}>Remove Last Layer</button>

                <button
                className="add-layer-button"
                onClick={() => {
                  if (firstLayerOutput > 0) {
                    setIsPopupOpen(true);
                  } else {
                    alert("Wrong output value.");
                  }
                }}
                >
                Add New Layer
              </button>
            </div>

            

            <div className="save-button">
              <button onClick={createModel}>
                Save model
              </button>
            </div>
          </div>
          {isPopupOpen ? openPopup() : null}
        </div>
      ) : (
        <div className="select-dataset-container">
          <div className="align-center">
            <select
              name="datasets"
              id="datasets"
              onChange={(item) => {
                var dataset = datasets.find((element) => {
                  return element.file_id.toString() === item.target.value;
                });
                setSelectedDataset(dataset);
              }}
            >
              <option disabled selected hidden>
                {" "}
                Select dataset{" "}
              </option>

              {datasets.map((item) => (
                <option value={item.file_id}>{item.file_name}</option>
              ))}
            </select>
          </div>

          {selectedDataset ? (
            <>
              <div className="columns-container">
                <form>
                  {selectedDataset.columns.map((element) => {
                    return (
                      <>
                        <div className="label-select-row">
                          <label htmlFor={element + "_column"} className="label-grid-item">
                            {element}{" "}
                          </label>
                          <select
                            className="select-grid-item"
                            name={element + "_column"}
                            id={element + "_column"}
                          >
                            <option value="categorical_columns">
                              Categorical
                            </option>
                            <option value="numerical_columns">Numerical</option>
                            <option value="output">Output</option>
                          </select>
                        </div>
                      </>
                    );
                  })}
                </form>
              </div>
              <div className="align-center">
                <button
                  onClick={() => {
                    let numerical = Array<String>();
                    let categorical = Array<String>();
                    let output: String = "";
                    const validate = () => {
                      let isOutputValid = false;
                      selectedDataset.columns.forEach((element) => {
                        let selectedType = document.getElementById(
                          element + "_column"
                        ) as HTMLSelectElement;
                        switch (selectedType.value) {
                          case "categorical_columns":
                            categorical.push(element);
                            break;
                          case "numerical_columns":
                            numerical.push(element);
                            break;
                          case "output":
                            isOutputValid = output === "";
                            output = element;
                            break;
                        }
                      });
                      return isOutputValid;
                    };
                    if (validate()) {
                     
                      setNumericalColumns(numerical)
                      setCategoricalColumns(categorical)
                      setOutputColumn(output) 
                      setIsSelectedDataset(true);
                    } else {
                      numerical = Array<String>();
                      categorical = Array<String>();
                      output = "";
                      alert(
                        "There has to be exactly 1 column marked as output."
                      );
                    }
                  }}
                >
                  Accept
                </button>
              </div>
            </>
          ) : null}
        </div>
      )}
      <div className="back-button">
        <Link to="/">
          <button>Back</button>
        </Link>
      </div>
    </>
  );
}
