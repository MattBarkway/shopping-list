<script lang="ts">
  import type { ActionData } from "./$types";
  import Login from "../../components/Login.svelte";

  export let form: ActionData;
</script>

<svelte:head>
  <title>Register</title>
</svelte:head>


<Login submitText="Register">
  <p>Already have an account?
    <a class="dark" href="/login">click here</a>
    to sign in
  </p>
  {#if form?.success}
    <p>Successfully registered! Check your emails to validate your account.</p>
  {/if}
  {#if form?.error}
    <p>Cockup alert: {form?.error}</p>
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
