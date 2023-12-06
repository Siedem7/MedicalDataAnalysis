import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import { logout } from '../Utils/ApiUtils'

import "./CreateAccount.css"

export default function CreateAccount() {
  const [groups, setGroups] = useState(["medical staff", "analyst", "admin"]);
  
  return (
    <>
      <div className="header">
        <h1>Create account</h1>
        <button onClick={logout}>log out</button>
      </div>
      <div className="create-account-form">
        <form>
          <div className="input-field">
            <label htmlFor="login">Insert login:</label>
            <input type="text" name="login" id="login" />
          </div>
          <div className="input-field">
            <label htmlFor="password">Insert password:</label>
            <input type="text" name="password" id="password" />
          </div>
          <div className="input-field">
            <p>Select new group:</p>
            <select name="users" id="users">
            <option disabled selected hidden> select group </option>
             {groups.map((item) => 
              <option value={item}>{item}</option>
              )}
            </select>
          </div>
        </form>
      </div>
      <div>
        <div className="add-user-button">
          <button>
            add user
          </button>
        </div>
        <div className="back-button">
          <Link to="/" >
            Back
          </Link>
        </div>
      </div>
    </>
  )
}