import React, { useState } from 'react'
import { getPermissions, logout } from '../Utils/ApiUtils';
import { Link } from "react-router-dom";

import './MainPage.css'

export default function MainPage() {
  
  let token = localStorage.getItem('token') as string
  const [permissions, setPermissions] = useState([""]);
  

  if (token === null) {
    window.location.href = '/login'
    return (<h1>Loading...</h1>)
  }
  
  if (permissions[0] === "") {
    getPermissions(token).then((result) => {
      setPermissions(result)
    });
  }

  let grid = "grid-" + permissions.length.toString();

  let projectPermisson = (item: string) =>{
    switch(item){
      case "DELETE_USER_ACCOUNT":
        return(
        <>
          <Link to="/account/delete" className="main-page-link" >
                <p>Delete account</p>
          </Link>
        </>
        )
      case "UPDATE_USER_ACCOUNT":
        return(
          <>
            <Link to="/account/update" className="main-page-link" >
                  <p>Update account</p>
            </Link>
          </>
          )
      case "CREATE_USER_ACCOUNT":
        return(
          <>
            <Link to="/account/create" className="main-page-link" >
                  <p>Create account</p>
            </Link>
          </>
          )
      case "MANAGE_PASSWORDS_POLICY":
        return(
          <>
            <Link to="/passwords_policy" className="main-page-link" >
                  <p>Manage passwords policy</p>
            </Link>
          </>
          )
      case "USE_MODEL":
        return(
          <>
            <Link to="/predict" className="main-page-link" >
                  <p>Predict disease</p>
            </Link>
          </>
          )
      case "VIEW_STATISTICS":
        return(
          <>
            <Link to="/statistics" className="main-page-link" >
                  <p>View statistics</p>
            </Link>
          </>
          )
      case "MANAGE_FILE":
        return(
          <>
            <Link to="/files" className="main-page-link" >
                  <p>Manage files</p>
            </Link>
          </>
          )
      case "CREATE_MODEL":
        return(
          <>
            <Link to="/create_model" className="main-page-link" >
                  <p>Create new model</p>
            </Link>
          </>
          )
    }
  } 

  return (
    <>
      <div className="header">
        <button onClick={logout}>log out</button>
      </div>
      <div className={grid + " main-page-container"}>
        {permissions.map((item) => 
          <div className="tile">
            {projectPermisson(item)}
          </div>
        )}
      </div>
    </>
  )

}