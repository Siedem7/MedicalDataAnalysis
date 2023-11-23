import React from 'react'

import { loginForm } from '../Utils/ApiUtils'
import './Login.css'

export default function Login() {
  const [username, setUsername] = React.useState('')
  const [password, setPassword] = React.useState('')

  return (
   <>
    <div className="container">
      <br />
      <form>
        <div className="input-line">
         <label htmlFor="username">Username</label>
         <input type="text" id="username" name="username" maxLength={32} value={username} onChange={(text) => setUsername(text.target.value)} />
        </div>
        <div className="input-line">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" maxLength={32} value={password} onChange={(text) => setPassword(text.target.value)}  />
        </div>
      </form>
      <div className="input-line">
        <button onClick={() => loginForm(username, password)}>Login</button>
      </div>
      <br />
    </div>
   </>     
  )

}