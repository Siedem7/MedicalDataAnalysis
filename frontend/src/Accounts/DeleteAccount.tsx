import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { getUsers, logout } from '../Utils/ApiUtils'

import './DeleteAccount.css'

export default function DeleteAccount() {
  let token = localStorage.getItem('token') as string
  const [users, setUsers] = useState([""]);

  if (users[0] === "") {
    getUsers(token).then((result) => {
      setUsers(result)
    });
  }

  return (
    <>
      <div className="header">
        <h1>Delete user account</h1>
        <button onClick={logout}>log out</button>
      </div>

      <div className="choose-user-container">
        <p>Choose user:</p>
        <select name="users" id="users">
         <option disabled selected hidden> select user </option>
          {
            users.map((item) =>
            <option value={item}>{item}</option>
          )}
        </select>
      </div>  

      <div className='delete-button'>
        <button>
          delete account
        </button>    
      </div>

      <div className="back-button">
        <Link to="/" >
          Back
        </Link>
      </div>
    </>
    )
  }