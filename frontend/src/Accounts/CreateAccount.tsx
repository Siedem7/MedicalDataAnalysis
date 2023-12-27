import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import { logout, getGroups, createUser } from '../Utils/ApiUtils'

import "./CreateAccount.css"

/**
 * React component responsible for creating a new user account.
 * @component
 * @returns {JSX.Element} Rendered JSX element.
 */
export default function CreateAccount() {
  // Retrieve the user token from local storage
  let token = localStorage.getItem('token') as string

  // State to store the list of groups, username, password, and selected group
  const [groups, setGroups] = useState([""])
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [group, setGroup] = useState('')
  
  // Fetch groups and update the state if it's empty
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
            Add User
          </button>
        </div>

        <div className="back-button">
          <Link to="/" >
            <button>Back</button>
          </Link>
        </div>

      </div>
    </>
  )
}