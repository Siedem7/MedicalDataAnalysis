import React, { useState, useEffect, Dispatch, SetStateAction } from "react";
import { Layer } from "./CreateModel";

export default function NewLayer(props: {
  setOpenPopup: Dispatch<SetStateAction<boolean>>;
  setLayers: Dispatch<SetStateAction<Array<Layer>>>;
  layers: Array<Layer>;
  inputSize: number;
}) {
  const [func, setFunc] = useState<string>("Linear");
  const [outputSize, setOutputSize] = useState<number>(1);

  return (
    <>
      <select name="function" id="" onChange={(ev) => setFunc(ev.target.value)}>
        <option value="Linear">Linear</option>
        <option value="Tanh">Tanh</option>
        <option value="ReLU">ReLU</option>
        <option value="Sigmoid">Sigmoid</option>
      </select>
      {func === "Linear" ? (
        <>
          <label htmlFor="input">Input: </label>
          <input
            type="number"
            name="input"
            id="input"
            value={props.inputSize.toString()}
            readOnly
          />
          <label htmlFor="output">Output:</label>
          <input
            type="number"
            name="output"
            id="output"
            onChange={(num) => setOutputSize(Number.parseInt(num.target.value))}
            value={outputSize}
          />
          <button
            onClick={() => {
              if (outputSize > 0) {
                props.layers.push({
                  function: func,
                  input: props.inputSize,
                  output: outputSize,
                });
                props.setLayers(props.layers);
                props.setOpenPopup(false);
              } else {
                alert("Output must be greater than 0.");
              }
            }}
          >
            Confirm
          </button>
        </>
      ) : (
        <>
          <button
            onClick={() => {
              props.layers.push({ function: func, input: null, output: null });
              props.setLayers(props.layers);
              props.setOpenPopup(false);
            }}
          >
            Confirm
          </button>
        </>
      )}
    </>
  );
}
