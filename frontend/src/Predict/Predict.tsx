import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom";
import { getAvailableModels, PredictionModel, getInputStructure, InputStrucure } from '../Utils/ApiUtils';
import { logout } from '../Utils/ApiUtils';
import PredictionInfo from './PredictionInfo'

import './Predict.css'

export default function Predict() {
    let token = localStorage.getItem("token") as string;
    const [isSelectedModel, setIsSelectedModel] = useState(false)
    const [selectedModel, setSelectedModel] = useState<PredictionModel>()
    const [models, setModels] = useState<Array<PredictionModel>>([])

    const [isPopupOpen, setIsPopupOpen] = useState<boolean>(false)
    const [probability, setProbability] = useState<number>(1)

    const[inputStructure, setInputStructure] = useState<InputStrucure>({
      categorical_columns: [],
      numerical_columns: [],
      output_column: '',
    })

    useEffect(()=> {
      getAvailableModels(token, setModels)
    }, [])

    const transformString = (text:string) =>{
        const words = text.split("_")
        const newString = words
        .map((word:string) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');

        return newString;
    }

    const sendPredict = () => {
        let patientData:{[key:string]:[any]} = {}

        inputStructure.categorical_columns.forEach((column)=>{
            var selectElement = (document.getElementById(column.name)) as HTMLSelectElement;
            column.values.forEach((value)=>{
                let property
                if(value === selectElement.value){
                    property =column.name + "_" + value 
                    patientData[property] = [true]
                }
                else{
                    property =column.name + "_" + value 
                    patientData[property] = [false]
                }
            })
        })  

        inputStructure.numerical_columns.forEach((column)=>{
            var inputElement = (document.getElementById(column.name)) as HTMLInputElement;
            var property = column.name
            var dataToProcess = (parseInt(inputElement.value)-column.min)/(column.max-column.min)
            dataToProcess = dataToProcess > 1 ? 1: dataToProcess
            dataToProcess = dataToProcess < 0 ? 0: dataToProcess
            patientData[property] = [dataToProcess]
        })

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", "Bearer " + token);
        
        var raw = JSON.stringify({"data": patientData});
        
        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw
        };
        
        fetch("http://127.0.0.1:5000/predict/" + selectedModel?.id, {...requestOptions, redirect:"follow"})
          .then(response => response.json())
          .then(result => setProbability(result["answer"]))
          .catch(error => console.log('error', error));
        
        setIsPopupOpen(true)
    }

    return (
      <>
        <div className="header">
            <h1>Predict Disease</h1>
            <button onClick={logout}>log out</button>
        </div>

        {isSelectedModel ?  
          <>
            <div className='input-data-container'>

                <div className='categorical-columns-container'>
                    {inputStructure.categorical_columns.map((column) => 
                    <>
                        <div className='data-input-row'>
                            <label htmlFor={column.name}>{transformString(column.name) + ": "}</label>
                            <select name={column.name} id={column.name}>
                                <option disabled selected hidden> select value </option>
                                {column.values.map((value) => <option value={value.toString()}>{transformString(value)}</option>)}
                            </select>
                        </div>      
                    </>)}
                </div>

                <div className='numerical-columns-container'>
                    {inputStructure.numerical_columns.map((column)=>
                    <>
                        <div className='data-input-row'>
                            <label htmlFor={column.name}>{transformString(column.name) + ": "}</label>
                            <input type="number" id={column.name} min={column.min} max={column.max}/>
                        </div>
                    </>)}
                </div>

            </div>

            <div className='predict-button-container'>
                <button onClick={()=>{sendPredict()}}>
                    Predict
                </button>
            </div>
            {isPopupOpen? <PredictionInfo probability={probability} setPopupOpen={setIsPopupOpen}></PredictionInfo> : null}
          </>
          :
          <>
            <div className='select-model-container'>
                <div className='model-input-row'>
                    <label htmlFor="select-model">Choose model: </label>
                    <select name="select-model" id="select-model" onChange={(ev) => {
                        var model = models.find((model) => { return model.id.toString() === ev.target.value })
                        setSelectedModel(model)
                    }}>
                    <option disabled selected hidden> select model </option>
                        {models.map((model:PredictionModel) => <option value={model.id.toString()}>{model.name}</option>)}
                    </select>
                </div>
            </div>
            <div className='save-model-button-container'>
                <button onClick={() => {
                    if (selectedModel !== undefined){
                        getInputStructure(token, setInputStructure, selectedModel.id)
                        setIsSelectedModel(true)
                    }
                    else{
                        alert("Select model first.")
                    }
                }}>
                    Save
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