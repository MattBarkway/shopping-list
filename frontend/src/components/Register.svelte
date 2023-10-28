<!-- Login.svelte -->

<script>
  let username = '';
  let password = '';
  let isLoading = false;
  let error = "";

  async function handleLogin() {
    isLoading = true;
    error = "";
    const data = new URLSearchParams();
    data.append("username", username);
    data.append("password", password);

    const response = await fetch('http://localhost:8000/api/v1/auth/token', {
        method: 'post',
        body: data,
    })
    if (!response.ok) {
      error = JSON.stringify(await response.json());
    }

    isLoading = false;
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
