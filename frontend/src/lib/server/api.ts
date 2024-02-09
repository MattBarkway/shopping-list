import { HOST_URL } from "$env/static/private";

interface Item {
  name: string;
  description: string;
  quantity: number;
}

// Items
export async function getItems(token: string, listID: string) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/items`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}

export async function addItem(token: string, listID: string, item: Item) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/items`, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(item)
  });
}

export async function getItem(listID: string, itemID: number) {
}

export async function removeItem(token: string, listID: string, itemID: number) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/items/${itemID}`, {
    method: "DELETE",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    }
  });
}

export async function updateItem(token: string, listID: string, itemID: number, item: Item) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/items/${itemID}`, {
    method: "PATCH",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(item)
  });
}

//Lists
export async function getLists(token: string) {
  return await fetch(`${HOST_URL}/api/v1/shopping/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}

export async function createList(token: string, name: string) {
  return await fetch(`${HOST_URL}/api/v1/shopping/`, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name })
  });
}

export async function updateList(name: string) {
} // Should maybe be ID?
export async function getList(token: string, listID: string) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}

export async function deleteList(listID: string) {
}

//Collaborators
export async function getCollaborators(listID: string) {
}

export async function addCollaborator(token: string, listID: string, email: string) {
  return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/collaborators`, {
    method: "PATCH",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ email })
  });
}

export async function validateCollaborator(token: string, listID: string, colabToken: string) {
    return await fetch(`${HOST_URL}/api/v1/shopping/${listID}/collaborators/validate/${colabToken}`, {
    method: "PATCH",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${token}`
    },
  });
}


export async function removeCollaborator(listID: string, userID: number) {
}

//Auth
export async function login(username: string, password: string) {
  const formData = new FormData();
  if (!username || !password) {
    throw new Error("You must provide a username and password!");
  }
  formData.append("username", username);
  formData.append("password", password);

  return await fetch(`${HOST_URL}/api/v1/auth/token`, {
    method: "POST",
    body: formData
  });
}

export async function register(username: string, password: string) {
  const formData = new FormData();
  if (!username || !password) {
    throw new Error("You must provide a username and password!");
  }
  formData.append("username", username);
  formData.append("password", password);

  return await fetch(`${HOST_URL}/api/v1/auth/register`, {
    method: "POST",
    body: formData
  });
}

export async function getUser(token: string) {
  return await fetch(`${HOST_URL}/api/v1/auth/user`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}


// TODO duplicated collaborator APIs in backend?
