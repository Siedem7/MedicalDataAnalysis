import React, { Dispatch, SetStateAction, useState, useEffect } from "react";
import { io, Socket } from "socket.io-client";

interface TrainingProgressProps {
  modelName: string;
  setIsTrainingInProgress: Dispatch<SetStateAction<boolean>>;
}

export default function TrainingProgress(props: TrainingProgressProps) {
  const [infoList, setInfoList] = useState<string[]>([]);   

  useEffect(() => {
    const socket: Socket = io("http://127.0.0.1:5000/", {
      withCredentials: true,
      extraHeaders: {
        "Access-Control-Allow-Origin": "http://localhost:3000/",
      },
    });

    socket.on(props.modelName, (arg: string) => {
      setInfoList(prevInfoList => [arg, ...prevInfoList]);
    });

    return () => {
      socket.disconnect();
    };
  }, [props.modelName]);

  return (
    <>
      <div className="popupBackground" 
            onClick={()=>{
            props.setIsTrainingInProgress(false);
            setInfoList([]);
          }}></div>
      <div className="popupForeground training-progress-popup">
        {infoList.map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </div>
    </>
  );
}