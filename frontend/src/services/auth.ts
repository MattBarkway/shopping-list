export function isAuthenticated() {
    const token = localStorage.getItem('authToken');
    return !!token;
}

export function login(username: string, password: string) {
    // Make a POST request to your backend's login endpoint
    // Store the received authentication token in localStorage
}

export function logout() {
    // Clear the authentication token from localStorage
}
