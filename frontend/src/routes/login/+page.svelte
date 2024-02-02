<script lang="ts">
  import type { ActionData } from "./$types";
  import Login from "../../components/Login.svelte";

  export let form: ActionData;
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>


<Login submitText="Log in">
  <p>New here? <a class="dark" href="/register">click here</a> to register</p>
  {#if form?.error}
    <p class="error">{form?.error}</p>
  {/if}
</Login>

<style>
    a {
        color: #dcdcdc;
    }

    .error {
        color: #ffafaf;
        font-weight: bold;
    }
</style>
