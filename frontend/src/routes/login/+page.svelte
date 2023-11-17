<script>
  import Login from "../../components/Login.svelte";
  import { isAuthenticated, login } from "$lib/auth";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let isLoading = false;

  let authenticated = false;

  onMount(() => {
    authenticated = isAuthenticated();
    if (authenticated) {
      goto("/");
    }
  });

  async function handleLogin(event) {
    console.log(event);
    isLoading = true;
    await login(event.detail.username, event.detail.password);
    isLoading = false;
    await goto("/");
  }

</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

<Login on:submit={handleLogin} isLoading={isLoading} />

<p>Don't have an account? <a href="/register">register here</a></p>
