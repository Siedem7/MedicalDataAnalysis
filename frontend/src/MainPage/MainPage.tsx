import React from 'react'
import { getPermissions } from '../Utils/ApiUtils';


export default function MainPage() {
  const [token, setToken] = React.useState('');

  if (localStorage.getItem('token') === null) {
    window.location.href = '/login'
  }
 
  setToken(localStorage.getItem('token') as string)
  let permissions = getPermissions(token)


  return (
    <>
      <h1>działa</h1>
    </>
  )

}