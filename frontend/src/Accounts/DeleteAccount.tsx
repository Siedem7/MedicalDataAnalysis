import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { getUsers, logout, deleteUser } from '../Utils/ApiUtils'

import './DeleteAccount.css'

/**
 * Functional component for deleting user accounts.
 * @returns {JSX.Element} JSX element representing the DeleteAccount component.
 */
export default function DeleteAccount() {
  // Retrieve the user token from local storage
  let token = localStorage.getItem('token') as string;
  let idToDelete: Number = -1;

  // State to store the list of users
  const [users, setUsers] = useState(Array<{ id: Number; login: String; }>);

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
        <h1>Delete user account</h1>
        <button onClick={logout}>log out</button>
      </div>

      <div className="delete-user-container">
        <p>Choose user:</p>
        <select name="userSelection" id="userSelection" onChange={(ev) => idToDelete = parseInt(ev.target.value)}>
         <option disabled selected hidden> Select User </option>
          {
            users.map((item) =>
            <option value={item.id.toString()}>{item.login}</option>
          )}
        </select>
      </div>  

      <div className='delete-button'>
        <button onClick={() =>
            {
              deleteUser(token, idToDelete)
              setUsers(users.filter((item) => { return item.id !== idToDelete }))
            }}>
          Delete User
        </button>    
      </div>

      <div className="back-button">
        <Link to="/" >
            <button>Back</button>
        </Link>
      </div>
    </>
    )
  }