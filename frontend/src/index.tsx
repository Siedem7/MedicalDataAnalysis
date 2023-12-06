import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';

import { Route, Routes } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';

import Login from './Login/Login';
import Logout from './Login/Logout';
import MainPage from './MainPage/MainPage';
import Predict from './Predict/Predict';
import CreateModel from './CreateModel/CreateModel';
import PasswordsPolicy from './PasswordsPolicy/PasswordsPolicy';
import FileManagement from './FileManagement/FileManagement';
import Statistics from './Statistics/Statistics';
import CreateAccount from './Accounts/CreateAccount'
import UpdateAccount from './Accounts/UpdateAccount'
import DeleteAccount from './Accounts/DeleteAccount'


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<MainPage />} />
      <Route path='/login' element={<Login />} />
      <Route path='/logout' element={<Logout />} />
      <Route path='/predict' element={<Predict />} />
      <Route path='/predict/:model_id' element={<Predict />} />
      <Route path='/create_model' element={<CreateModel />} />
      <Route path='/passwords_policy' element={<PasswordsPolicy />} />
      <Route path='/files' element={<FileManagement />} />  
      <Route path='/files/:file_id' element={<FileManagement />} />
      <Route path='/statistics' element={<Statistics />} /> 
      <Route path='/account/create' element = {<CreateAccount />} />
      <Route path='/account/update' element = {<UpdateAccount />} />
      <Route path='/account/delete' element = {<DeleteAccount />} />
      <Route path='*' element={<h1>404</h1>} />

    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
