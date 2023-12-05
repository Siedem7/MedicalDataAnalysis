import React, { useState } from 'react'
import { getPermissions } from '../Utils/ApiUtils';
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

  let grid = "grid" + permissions.length.toString();

  //switch link+img
  return (
    <>
      <div className="main-page-container">
        <div className={grid}>
          {permissions.map((item) => 
            <div className="tile">
              <Link to="/" className="main-page-link" >
                  <p>{item}</p>
              </Link>
            </div>
          )}
        </div>
      </div> 
    </>
  )

}