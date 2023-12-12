import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { getUsers, logout } from '../Utils/ApiUtils'

import './DeleteAccount.css'

/**
 * Functional component for deleting user accounts.
 * @returns {JSX.Element} JSX element representing the DeleteAccount component.
 */
export default function DeleteAccount() {
  // Retrieve the user token from local storage
  let token = localStorage.getItem('token') as string;
  
  // State to store the list of users
  const [users, setUsers] = useState([""]);

  // Fetch users and update the state if it's empty
  if (users[0] === "") {
    getUsers(token).then((result) => {
      // Map the user objects to strings containing id and login
      setUsers(result.map(user => `${user.id}:${user.login}`));
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