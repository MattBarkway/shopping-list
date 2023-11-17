<!-- Login.svelte -->

<script>
  let username = '';
  let password = '';
  let isLoading = false;
  let error = "";

  async function login() {
    // Send a request to your backend server here
    // You can use the Fetch API or an HTTP library like Axios
    error = "";
    const formData = new FormData();
    formData.append("grant_type", "password");
    if ( !username || !password) {
      error = "You must provide a username and password!";
      return;
    }
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/token', {
        method: 'POST',
        body: formData, // Send form data
      });

      if (response.ok) {
        let data = await response.json()
        userStore.setAccessToken(data.access_token);
      } else {
        if (response.status === 401) {
          error = "Invalid credentials!"
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
</script>

<main>
  <h1>Login</h1>
  <form on:submit={handleLogin}>
    <label for="username">Username:</label>
    <input type="text" id="username" bind:value={username} required />

    <label for="password">Password:</label>
    <input type="password" id="password" bind:value={password} required />

    {#if error}
      <p class="error">{error}</p>
    {/if}

    <button type="submit" disabled={isLoading}>
      {isLoading ? 'Logging in...' : 'Login'}
    </button>
  </form>
</main>

<style>
  h1 {
    font-size: 24px;
    margin-bottom: 16px;
  }

  label {
    display: block;
    margin-bottom: 8px;
  }

  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 16px;
    border: 1px solid #ccc;
  }

  .error {
    color: red;
    margin-top: 8px;
  }

  button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
</style>
