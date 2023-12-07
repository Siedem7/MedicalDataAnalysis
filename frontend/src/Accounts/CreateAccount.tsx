import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import { logout, getGroups, createUser } from '../Utils/ApiUtils'

import "./CreateAccount.css"

export default function CreateAccount() {
  let token = localStorage.getItem('token') as string
  const [groups, setGroups] = useState([""]);
  const [username, setUsername] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [group, setGroup] = React.useState('')
  
  if (groups[0] === "") {
    getGroups(token).then((result) => {
      setGroups(result)
    });
  }

  return (
    <>
      <div className="header">
        <h1>Create account</h1>
        <button onClick={logout}>log out</button>
      </div>

      <div className="create-account-form">
        <form>
          <div className="input-field">
            <label htmlFor="username">Insert username:</label>
            <input type="text" name="username" id="username" maxLength={32} value={username} onChange={(text) => setUsername(text.target.value)} />
          </div>

          <div className="input-field">
            <label htmlFor="password">Insert password:</label>
            <input type="text" name="password" id="password" maxLength={32} value={password} onChange={(text) => setPassword(text.target.value)}/>
          </div>

          <div className="input-field">
            <p>Select new group:</p>
            <select name="users" id="users" value={group} onChange={(text) => setGroup(text.target.value)}>
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
          <button onClick={() => createUser(token, username, password, group)}>
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