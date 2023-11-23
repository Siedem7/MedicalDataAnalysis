import React from 'react'

import { loginForm } from '../Utils/ApiUtils'

export default function Login() {
  const [username, setUsername] = React.useState('')
  const [password, setPassword] = React.useState('')

  return (
   <>
    <h1>Login page</h1>
    <form>
      <label htmlFor="username">Username</label>
      <input type="text" id="username" name="username" value={username} onChange={(text) => setUsername(text.target.value)} />
      <label htmlFor="password">Password</label>
      <input type="password" id="password" name="password" value={password} onChange={(text) => setPassword(text.target.value)}  />
    </form>
    <button onClick={() => loginForm(username, password)}>Login</button>
   </>     
  )

}