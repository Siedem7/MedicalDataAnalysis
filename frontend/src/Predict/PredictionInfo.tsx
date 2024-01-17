import React, { Dispatch, SetStateAction} from "react";

interface PredictionInfoProps {
    probability: number;
    setPopupOpen: Dispatch<SetStateAction<boolean>>;
}

export default function PredictionInfo(props: PredictionInfoProps) { 

  return (
    <>
      <div className="popupBackground " 
            onClick={()=>{
            props.setPopupOpen(false)
          }}></div>
      <div className="popupForeground">
          <h2>Disease probability: {props.probability}</h2>
      </div>
    </>
  );
}