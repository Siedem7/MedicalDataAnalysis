import React, { useState } from 'react'
import { getPermissions } from '../Utils/ApiUtils';
import { Link } from "react-router-dom";

import './MainPage.css'

export default function MainPage() {
  let token = localStorage.getItem('token') as string
  const [permissions, setPermissions] = useState([""]);

  if (token === null) {
    window.location.href = '/login'
  }
  
  if (permissions[0] === "") {
    getPermissions(token).then((result) => {
      setPermissions(result)
    });
  }

  return (
    <>
      <div className="main-page-container">
        {permissions.map((item) => 
          <Link to="/">
            <div className="tile">
              {item}
            </div>
          </Link>
        )}
      </div>
    </>
  )

}