export async function login(username: string, password: string) {
	const formData = new FormData();
	formData.append('grant_type', 'password');
	if (!username || !password) {
		throw new Error('You must provide a username and password!');
	}
	formData.append('username', username);
	formData.append('password', password);

	const response = await fetch('http://localhost:8000/api/v1/auth/token', {
		method: 'POST',
		body: formData,
	});

	if (response.ok) {
		let data = await response.json();
		localStorage.setItem("authToken", data['access_token']);
	} else {
		if (response.status === 401) {
			throw new Error('Invalid credentials!');
		}
	}
}

export function logout() {
	localStorage.removeItem("authToken");
}

export function isAuthenticated() {
	const token = localStorage.getItem('authToken');
	return !!token;
}
