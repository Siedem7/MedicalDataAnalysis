export function loginForm(login: string, password: string) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "login": login,
    "password": login
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
          console.log(localStorage.getItem('token'))
        })
        window.location.href = '/'
      }
      else {
        alert('Wrong login or password.')
      }
    })
    .catch(error => console.log('error', error));

}