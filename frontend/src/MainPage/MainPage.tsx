import React, { useState } from 'react'
import { getPermissions } from '../Utils/ApiUtils';


export default function MainPage() {
  let token = localStorage.getItem('token') as string
  const [permissions, setPermissions] = useState([""]);

  if (token === null) {
    window.location.href = '/login'
  }
  
  if (permissions[0] === "") {
    getPermissions(token).then((result) => {
      setPermissions(result)
    });
  }

  return (
    <>
      <h1>test</h1>
      <h1>{permissions.map((item) => <h1>{item}</h1>)}</h1>
    </>
  )

}