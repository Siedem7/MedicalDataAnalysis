/**
 * Represents a data set with information about a file.
 * @interface DataSet
 */
export interface DataSet {
  /**
   * The unique identifier for the file.
   * @type {number}
   */
  file_id: number;

  /**
   * The name of the file.
   * @type {string}
   */
  file_name: string;

  /**
   * A brief description of the data set.
   * @type {string}
   */
  description: string;

  /**
   * An array containing the names of columns in the data set.
   * @type {string[]}
   */
  columns: string[];
}



export function loginForm(login: string, password: string) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    login: login,
    password: password,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("http://127.0.0.1:5000/login", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 200) {
        response.text().then((text) => {
          let token = JSON.parse(text).token;
          localStorage.setItem("token", token);
        });
        window.location.href = "/";
      } else {
        alert("Error occured.");
      }
    })
    .catch((error) => console.log("error", error));
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

export async function getPermissions(token: string): Promise<string[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: "GET",
    headers: myHeaders,
  };

  return await fetch("http://127.0.0.1:5000/permissions", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 401) {
        window.location.href = "/login";
        throw new Error("Unauthorized");
      } else {
        return response.text().then((text) => {
          return JSON.parse(text).permissions as string[];
        });
      }
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export async function getGroups(token: string): Promise<string[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: "GET",
    headers: myHeaders,
  };

  return await fetch("http://127.0.0.1:5000/groups", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      return response.text().then((text) => {
        return JSON.parse(text).groups as string[];
      });
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export async function getUsers(
  token: string
): Promise<{ id: Number; login: String }[]> {
  var myHeaders = new Headers();
  myHeaders.append("Authorization", "Bearer " + token);

  var requestOptions = {
    method: "GET",
    headers: myHeaders,
  };

  return await fetch("http://127.0.0.1:5000/users", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 403) {
        throw new Error("Permission denied");
      } else {
        return response.json().then((data) => {
          let temp: { id: number; login: string }[] = [];
          for (let i = 0; i < data.users.length; i++) {
            temp.push({
              id: data.users[i].id,
              login: data.users[i].login,
            });
          }
          return temp;
        });
      }
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export function createUser(
  token: string,
  login: string,
  password: string,
  group: string
) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", "Bearer " + token);

  var raw = JSON.stringify({
    login: login,
    password: password,
    group: group,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("http://127.0.0.1:5000/create_user", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 403) {
        throw new Error("Permission denied");
      } else if (response.status === 200) {
        return response.text().then((text) => {
          alert(text);
        });
      } else {
        alert("Error occured.");
      }
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export function deleteUser(token: String, id: Number) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", "Bearer " + token);

  var raw = JSON.stringify({
    user_id: id,
  });

  var requestOptions = {
    method: "DELETE",
    headers: myHeaders,
    body: raw,
  };

  fetch("http://127.0.0.1:5000/delete_user", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 403) {
        throw new Error("Permission denied");
      } else if (response.status === 200) {
        return response.text().then((text) => {
          alert(text);
        });
      } else {
        alert("User is not deleted. Error occured.");
      }
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export function updateUser(
  token: String,
  id: Number,
  login: String,
  password: String,
  group: String
) {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", "Bearer " + token);

  var raw = JSON.stringify({
    user_id: id,
    login: login,
    password: password,
    group: group,
  });

  var requestOptions = {
    method: "PUT",
    headers: myHeaders,
    body: raw,
  };

  fetch("http://127.0.0.1:5000/update_user", {
    ...requestOptions,
    redirect: "follow",
  })
    .then((response) => {
      if (response.status === 403) {
        throw new Error("Permission denied");
      } else if (response.status === 200) {
        return response.text().then((text) => {
          alert(text);
        });
      } else {
        alert("User is not updated. Error occured.");
      }
    })
    .catch((error) => {
      console.log("error", error);
      throw error;
    });
}

export function getAvailableDatasets(token: String, setDataSet: React.Dispatch<React.SetStateAction<DataSet[]>>) {
  var myHeaders = new Headers();
  myHeaders.append(
    "Authorization",
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI1ODA5NjMsImlhdCI6MTcwMjQ5NDU2Mywic3ViIjoyfQ.-RSDOCGRbbBI_7Rk440FiorcLKaELS8bknWYojwfRss"
  );

  var requestOptions = {
    method: "GET",
    headers: myHeaders
  };

  fetch("http://127.0.0.1:5000/get_datasets", {...requestOptions, redirect: "follow"})
    .then((response) => response.json())
    .then((result) => setDataSet(result))
    .catch((error) => console.log("error", error));
}
