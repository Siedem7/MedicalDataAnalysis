export function loginForm(login: string, password: string) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "login": login,
    "password": password
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw
  };

  fetch("http://127.0.0.1:5000/login", { ...requestOptions, redirect: 'follow' })
    .then(response => {
      if (response.status === 200) {
        response.text().then((text) => {
          let token = JSON.parse(text).token
          localStorage.setItem('token', token)
        })
        window.location.href = '/'
      }
      else {
        alert('Wrong login or password.')
      }
    })
    .catch(error => console.log('error', error));
}

export function logout() {
  localStorage.removeItem('token')
  window.location.href = '/login'
}

export async function getPermissions(token: string): Promise<string[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
  };
  
  return await fetch("http://127.0.0.1:5000/permissions", { ...requestOptions, redirect: 'follow' })
    .then(response => {
      if (response.status === 401) {
        window.location.href = '/login';
        throw new Error('Unauthorized');
      } else {
        return response.text().then((text) => {
          return JSON.parse(text).permissions as string[];
        });
      }
    })
    .catch(error => {
      console.log('error', error);
      throw error;
    });
}

export async function getGroups(token: string): Promise<string[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: 'GET',
    headers: myHeaders
  };

  return await fetch("http://127.0.0.1:5000/groups", { ...requestOptions, redirect: 'follow' })
    .then(response => {
        return response.text().then((text) => {
          return JSON.parse(text).groups as string[];
      });
    })
    .catch(error => {
      console.log('error', error);
      throw error;
    });
}

export async function getUsers(token: string): Promise<string[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
  };
  
  return await fetch("http://127.0.0.1:5000/users", { ...requestOptions, redirect: 'follow' })
    .then(response => {
      if (response.status === 401) {
        throw new Error('Unauthorized');
      } else {
        return response.text().then((text) => {
          let temp:string[] = [];
          for(let i = 0; i < JSON.parse(text).users.length; i++){
            temp.push(JSON.parse(text).users[i].login);
          }
          return temp;
        });
      }
    })
    .catch(error => {
      console.log('error', error);
      throw error;
    });
}

export function createUser(token: string, login: string, password: string, group: string) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", "Bearer " + token);

  var raw = JSON.stringify({
    "login": login,
    "password": password,
    "group": group
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw
  };
  
  fetch("http://127.0.0.1:5000/users", { ...requestOptions, redirect: 'follow' })
    .then(response => {
      if (response.status === 401) {
        throw new Error('Unauthorized');
      } 
      else if (response.status === 200){
        return response.text().then((text) => {
          console.log(text);
        });
      }
      else{
        alert("No username or password.")
      }
    })
    .catch(error => {
      console.log('error', error);
      throw error;
    });
}
