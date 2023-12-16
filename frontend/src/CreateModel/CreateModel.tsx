import React, { useState, useEffect } from "react";
import { getAvailableDatasets, logout, DataSet } from "../Utils/ApiUtils";
import { Link } from "react-router-dom";

import "./CreateModel.css";

/**
 * Represents an interface for a layer.
 * @interface
 */
interface Layer {
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

  let numericalColumns = Array<String>()
  let categoricalColumns =  Array<String>()
  let outputColumn: String = ""

  const [layers, setLayers] = useState([
    { function: "Tanh", input: null, output: null },
    { function: "Linear", input: 10, output: 15 },
    { function: "Linear", input: 15, output: 20 },
    { function: "Linear", input: 20, output: 10 },
    { function: "ReLU", input: null, output: null },
    { function: "Linear", input: 10, output: 1 },
  ]);

  const [firstLayerOutput, setFirstLayerOutput] = useState(10)
  const [datasets, setDatasets] = useState<Array<DataSet>>([]);
  const [selectedDataset, setSelectedDataset] = useState<DataSet>()
  const [isSelectedDataset, setIsSelectedDataset] = useState(false)

  useEffect(() => {
    getAvailableDatasets(token, setDatasets);
  }, []);
  const addLayer = () => {
    setLayers( [
      { function: "NewLayer", input: null, output: null },
    ]);
  };

  return (
    <>
      <div className="header">
        <h1>Create model</h1>
        <button onClick={logout}>log out</button>
      </div>
      {isSelectedDataset ? (
        <div>
          <div className="layer-container">
            <div className="layer input-layer">
              <label htmlFor="first-layer-input">Output:</label>
              <input
                type="text"
                name="first-layer-input"
                id="first-layer-input"
              />
            </div>

            {layers.map((layer: Layer) => (
              <div className="layer" key={layer.function}>
                {layer.input === null ? (
                  layer.function
                ) : (
                  <div>
                    {layer.function} Input: {layer.input} Output: {layer.output}
                  </div>
                )}
              </div>
            ))}

            <div className="layer output-layer">Sigmoid</div>
          </div>
          <div>
            <button>Check</button>
          </div>
          <button onClick={()=>{setIsSelectedDataset(false)}}>
            Change Dataset
          </button>
          <button className="add-layer-button" onClick={addLayer}>
            Add Layer
          </button>
        </div>
      ) : (
        <div>
          <select
            name="datasets"
            id="datasets"
            onChange={(item) => {
              var dataset = datasets.find((element) => {
                return element.file_id.toString() === item.target.value;
              });
              setSelectedDataset(dataset)
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

          {selectedDataset ? 
          <>
            <form action="">
            {selectedDataset.columns.map((element) => {
              return (
              <>
                <label  htmlFor={element + "_column"}>{element}</label>
                <select name={element + "_column"} id={element + "_column"} >
                  <option value="categorical_columns">Categorical</option>
                  <option value="numerical_columns">Numerical</option>
                  <option value="output">Output</option>
                </select>
                <br></br>
              </>
              )
            })}
            </form>
            <button onClick={() => {
              const validate = () => {
                  let isOutputValid = false;
                  selectedDataset.columns.map((element) => {
                  
                  let selectedType = document.getElementById(element + "_column") as HTMLSelectElement
                  switch (selectedType.value) {
                    case "categorical_columns": 
                      categoricalColumns.push(element)
                      break
                    case "numerical_columns":
                      numericalColumns.push(element)
                      break
                    case "output":
                      isOutputValid = outputColumn === ""
                      outputColumn = element
                      break
                  }
                })
                return isOutputValid
              }
              if (validate()) {
                setIsSelectedDataset(true) 
              }
              else {
                numericalColumns = Array<String>()
                categoricalColumns =  Array<String>()
                outputColumn = ""
                alert("There has to be exactly 1 column marked as output.")
              }
              }}>Accept</button>
          </> 
          : null}
        </div>
      )}
      <div className="back-button">
        <Link to="/">Back</Link>
        </div>
        <div className="create-model-button">Create Model</div>
        <div className="insert-training-data-button">
          Insert Training Data (File Dialog)
        </div>
        <div className="preprocess-data-button">Preprocess Data</div>
      </>
  );
  
}
