import React, {
  useState,
  useEffect,
  Dispatch,
  SetStateAction,
  MouseEventHandler,
} from "react";
import { Layer } from "./CreateModel";

export default function NewLayer(props: {
  setOpenPopup: Dispatch<SetStateAction<boolean>>;
  setLayers: Dispatch<SetStateAction<Array<Layer>>>;
  layers: Array<Layer>;
  inputSize: number;
}) {
  const [func, setFunc] = useState<string>("Linear");
  const [outputSize, setOutputSize] = useState<number>(1);

  const buttons = (onConfirm: MouseEventHandler<HTMLButtonElement>) => {
    return (
      <>
      <div className="new-layer-buttons">
        <button
          onClick={() => {
            props.setOpenPopup(false);
          }}
        >
          Cancel
        </button>
        <button onClick={onConfirm}>Confirm</button>
      </div>
      </>
    );
  };

  return (
  <>
  <div className="popupBackground"></div>
    <div className="popupForeground">
      <select name="function" id="" onChange={(ev) => setFunc(ev.target.value)}>
        <option value="Linear">Linear</option>
        <option value="Tanh">Tanh</option>
        <option value="ReLU">ReLU</option>
        <option value="Sigmoid">Sigmoid</option>
      </select>
      {func === "Linear" ? (
        <>
          <div className="new-layer-input">
            <label htmlFor="input">Input: </label>
            <input
              type="number"
              name="input"
              id="input"
              value={props.inputSize.toString()}
              readOnly
            />
          </div>
          <div className="new-layer-output">
            <label htmlFor="output">Output: </label>
            <input
              type="number"
              name="output"
              id="output"
              onChange={(num) => setOutputSize(Number.parseInt(num.target.value))}
              value={outputSize}
            />
          </div>
        </>
      ) : null}
      {buttons(()=>{
        if(func === "Linear"){
          if (outputSize > 0) {
            props.layers.push({
              function: func,
              input: props.inputSize,
              output: outputSize,
            });
            props.setLayers(props.layers);
            props.setOpenPopup(false);
          } 
          else {
            alert("Output must be greater than 0.");
          }
        }
        else{
          props.layers.push({ function: func, input: null, output: null })
          props.setOpenPopup(false)
          props.setLayers(props.layers)
        }})}
    </div>
  </>
  );
}
