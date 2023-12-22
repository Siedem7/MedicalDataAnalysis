import React, { useState, useEffect } from "react"
import { getAvailableDatasets, logout, DataSet } from "../Utils/ApiUtils"
import { Link } from "react-router-dom"
import  NewLayer  from "./NewLayer"
 
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

  let numericalColumns = Array<String>()
  let categoricalColumns =  Array<String>()
  let outputColumn: String = ""

  let batchSize: Number = 0;
  let epochsAmount: Number = 0
  let trainingPercent: Number = 0

  let description: String = ""
  let modelName: String = ""

  const [layers, setLayers] = useState<Array<Layer>>([]);

  const [firstLayerOutput, setFirstLayerOutput] = useState(10)
  const [datasets, setDatasets] = useState<Array<DataSet>>([]);
  const [selectedDataset, setSelectedDataset] = useState<DataSet>()
  const [isSelectedDataset, setIsSelectedDataset] = useState(false)
  const [isPopupOpen, setIsPopupOpen] = useState(false)

  const openPopup = () => {
    let inputSize = 0
    if (layers.length === 0) {
      inputSize = firstLayerOutput
    }
    else {
      for (var i = layers.length - 1; i >= 0; i--) {
        if (layers[i].output !== null) {
          inputSize = layers[i].output!
          break
        }
      }
      inputSize = inputSize === 0 ? firstLayerOutput : inputSize 
    }
    
    return <NewLayer setOpenPopup={setIsPopupOpen} layers={layers} setLayers={setLayers} inputSize={inputSize}/>
  }

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
              <label htmlFor="model-name">Insert model name: </label>
              <input type="text" id="model-name" name="model-name"/>
              <label htmlFor="description">Insert model description: </label>
              <textarea name="description" id="description" cols={30} rows={5}></textarea>
            </div>

            <div className="layer-container column">
              <div className="layer input-layer">
                <label htmlFor="first-layer-input">Output:</label>
                <input
                  type="number"
                  name="first-layer-input"
                  id="first-layer-input"
                  onChange={(event) => setFirstLayerOutput(Number.parseInt(event.target.value))}
                  value={firstLayerOutput}
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

            <div className="column right-column">
              <div>
                <label htmlFor="batch-size">Insert batch size: </label>
                <input type="number" name="batch-size" id="batch-size" />
              </div>
              <div>
                <label htmlFor="epochs-number">Insert number of epochs: </label>
                <input type="number" name="epochs-number" id="epochs-number" />
              </div>
              <div>
                <label htmlFor="training-percent">Insert training percent: </label>
                <input type="number" name="training-percent" id="training-percent" />
              </div>
            </div>
          </div>
          
          <div>
            <button>Check</button>
          </div>
          <button onClick={()=>{setIsSelectedDataset(false)}}>
            Change Dataset
          </button>
          <button className="add-layer-button" onClick={()=>{
            if(firstLayerOutput > 0){
              setIsPopupOpen(true)
            }
            else{
              alert("Wrong output value.")
            }

            }}>
            Add New Layer 
          </button>
          {isPopupOpen? openPopup() : null}
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
                  selectedDataset.columns.forEach((element) => {
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
      </>
  );
  
}
