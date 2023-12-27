import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom";
import { getAvailableModels, PredictionModel, getInputStructure, InputStrucure } from '../Utils/ApiUtils';
import { logout } from '../Utils/ApiUtils';

import './Predict.css'

export default function Predict() {
    let token = localStorage.getItem("token") as string;
    const [isSelectedModel, setIsSelectedModel] = useState(false)
    const [selectedModel, setSelectedModel] = useState<PredictionModel>()
    const [models, setModels] = useState<Array<PredictionModel>>([])

    const[inputStructure, setInputStructure] = useState<InputStrucure>({
      categorical_columns: [],
      numerical_columns: [],
      output_column: '',
    })

    useEffect(()=> {
      getAvailableModels(token, setModels)
    }, [])

    return (
      <>
        <div className="header">
            <h1>Predict Disease</h1>
            <button onClick={logout}>log out</button>
        </div>

        {isSelectedModel ?  
          <>
            <div className='input-data-container'>
                {inputStructure.categorical_columns.map((column) => 
                <>
                    <div className='data-input-row'>
                        <p>{column.name}</p>
                        <select name={column.name} id={column.name}>
                            <option disabled selected hidden> select value </option>
                            {column.values.map((value) => <option value={value.toString()}>{value}</option>)}
                        </select>
                    </div>  
                </>)}
                {inputStructure.numerical_columns.map((column)=>
                <>
                    <div className='data-input-row'>
                        <label htmlFor={column.name}>{column.name + ": "}</label>
                        <input type="number" min={column.min} max={column.max}/>
                    </div>
                </>)}

            </div>
          </>
          :
          <>
            <div className='select-model-container'>
                <p>Choose model:</p>
                <select name="select-model" id="select-model" onChange={(ev) => {
                    var model = models.find((model) => { return model.id.toString() === ev.target.value })
                    setSelectedModel(model)
                }}>
                <option disabled selected hidden> select model </option>
                    {models.map((model:PredictionModel) => <option value={model.id.toString()}>{model.name}</option>)}
                </select>
                <button onClick={() => {
                    if (selectedModel !== undefined){
                        getInputStructure(token, setInputStructure)
                        setIsSelectedModel(true)
                    }
                    else{
                        alert("Select model first.")
                    }
                }}>
                    Select model
                </button>
            </div>
          </>
        }

        <div className="back-button">
            <Link to="/">
                <button>Back</button>
            </Link>
        </div>
      </>
        
    )
}