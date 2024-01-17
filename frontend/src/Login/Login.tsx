import React from 'react'

import { loginForm } from '../Utils/ApiUtils'
import './Login.css'

export default function Login() {
  const [username, setUsername] = React.useState('')
  const [password, setPassword] = React.useState('')

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      loginForm(username, password)
    }
  };

  return (
   <>
    <div className="container-login" onKeyDown={handleKeyDown}>
      <br />
      <form>
        <div className="input-div">
         <label className="label-login" htmlFor="username">Username</label>
         <input className="input-login" type="text" id="username" name="username" maxLength={32} value={username} onChange={(text) => setUsername(text.target.value)} />
        </div>
        <div className="input-div">
          <label className="label-login" htmlFor="password">Password</label>
          <input className="input-login" type="password" id="password" name="password" maxLength={32} value={password} onChange={(text) => setPassword(text.target.value)}  />
        </div>
      </form>
      <div className="input-line">
        <button className="button-login" onClick={() => loginForm(username, password)}>Login</button>
      </div>
      <br />
    </div>
   </>     
  )

}