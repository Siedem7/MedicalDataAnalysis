import React, { useState } from "react";
import { logout } from "../Utils/ApiUtils";

import "./FileManagement.css";
import { Link } from "react-router-dom";

export default function FileManagement() {
  const [description, setDescription] = useState("");
  const [filePath, setFilePath] = useState("");

  const uploadFile = () => {
    let token = localStorage.getItem("token") as string;
    let fileInput = document.getElementById("file") as HTMLInputElement;

    if (fileInput === null ||
        fileInput.files === null || 
        description === "" ||
        fileInput.files[0] === undefined) {
      alert("Invalid input.")
      return
    }
    
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Bearer " + token);

    var formdata = new FormData();
    formdata.append(
      "csv_file",
      fileInput.files[0],
      filePath.split(/(\\|\/)/g).pop()
    );
    formdata.append("description", description);

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: formdata,
    };

    fetch("http://127.0.0.1:5000/upload_file", {
      ...requestOptions,
      redirect: "follow",
    })
      .then((response) => {
        if (response.status === 403) {
          throw new Error("Permission denied");
        } else if (response.status === 200) {
          return response.text().then((text) => {
            alert(text);
          });
        } else {
          alert("Error occured.");
        }
      })
      .catch((error) => {
        console.log("error", error);
        throw error;
      });
  };

  return (
    <>
      <div className="header">
        <h1>Manage Files</h1>
        <button onClick={logout}>log out</button>
      </div>

      <div className="file-input">
        <label htmlFor="description">Description: </label>
        <textarea
          required
          name="description"
          id="description"
          cols={30}
          rows={5}
          onChange={(text) => {
            setDescription(text.target.value);
          }}
        ></textarea>
        <input
          type="file"
          name="file"
          id="file"
          accept=".csv"
          onChange={(filePath) => {
            setFilePath(filePath.target.value);
          }}
        />
      </div>

      <div className="save-file-button-container">
        <button onClick={uploadFile}>Save file</button>
      </div>

      <div className="back-button">
        <Link to="/">
          <button>Back</button>
        </Link>
      </div>
    </>
  );
}
