import React, { useState } from "react";
import { logout, getGroups, getUsers, updateUser } from "../Utils/ApiUtils";
import { Link } from "react-router-dom";

import "./UpdateAccount.css"

/**
 * Functional component for updating user accounts.
 * @returns {JSX.Element} JSX element representing the UpdateAccount component.
 */
export default function UpdateAccount() {
  // Retrieve the user token from local storage
  let token = localStorage.getItem('token') as string

  // State to store the list of groups and users
  const [groups, setGroups] = useState([""])
  const [users, setUsers] = useState(Array<{ id: Number; login: String; }>)

  const [login, setLogin] = useState("")
  const [password, setPassword] = useState("")
  const [group, setGroup] = useState("")
  const [id, setId] = useState(-1)

  // Fetch groups and update the state if it's empty
  if (groups[0] === "") {
    getGroups(token).then((result) => {
      setGroups(result)
    });
  }

  // Fetch users and update the state if it's empty
  if (users.length === 0) {
    getUsers(token).then((result) => {
      // Map the user objects to strings containing id and login
      setUsers(result);
    });
  }
  
  return (
    <>
      <div className="header">
        <h1>Update user account</h1>
        <button onClick={logout}>log out</button>
      </div>

      <div className="choose-user-container">
        <p>Choose user:</p>
        <select name="users" id="users" onChange={(ev) => setId(parseInt(ev.target.value))}>
         <option disabled selected hidden> select user </option>
          { users.map((item) => <option value={item.id.toString()}>{item.login}</option> )}
        </select>
      </div>  
        
      <div className="update-account-form">
        <form>

          <div className="input-field">
            <label htmlFor="login">Insert new login:</label>
            <input type="text" name="login" id="login" maxLength={32} value={login} onChange={(text) => setLogin(text.target.value)}/>
          </div>

          <div className="input-field">
            <label htmlFor="password">Insert new password:</label>
            <input type="text" name="password" id="password" maxLength={32} value={password} onChange={(text) => setPassword(text.target.value)}/>
          </div>

          <div className="input-field">
            <p>Select new group:</p>
            <select name="users" id="users" onChange={(text) => setGroup(text.target.value)}>
              <option disabled selected hidden> select group </option>
              { groups.map((item) => <option value={item}>{item}</option> )}
            </select>
          </div>

        </form>
      </div>
      
      <div className="save-changes-button">
        <button onClick={()=>{
            setUsers(users.map((user) => { 
              if(user.id === id) { user.login = login }
              return user
            }))
            updateUser(token, id, login, password, group)
          }}>
          Save changes
        </button>
      </div>

      <div className="back-button">
        <Link to="/" >
         <button>Back</button>
        </Link>
      </div>
    </>
  );
}
