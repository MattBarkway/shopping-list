<script lang="ts">
  import github from "$lib/images/github.svg";
  import { Hamburger } from "svelte-hamburgers";
  import Menu from "../components/Menu.svelte";
  import type { LayoutData } from './$types';
  import { fly } from "svelte/transition";

  export let data: LayoutData;
  let open = false;
  let ready = true;
  $: menuItems = data.signed_in ?  { "Home 🏠": "/", "Logout 🚶": "/logout", "About ❓": "/about" }: { "Home 🏠": "/", "Login 🧍": "/login", "About ❓": "/about" };

</script>

<Hamburger bind:open --color="#dddddd" />
<Menu bind:open bind:ready bind:menuItems />

<div class="app">
  {#if !open && ready}
    <div class="fill" transition:fly={{ y: 195 }}>
      <main>
        <slot />
      </main>
    </div>
  {/if}
  <footer>
    <div class="corner">
      <a href="https://github.com/mattbarkway/shopping-list" target="_blank">
        <img src={github} alt="GitHub" />
      </a>
    </div>
  </footer>
</div>

<style>
    .fill {
        width: 100%;
        /*height: 90%;*/
        display: flex;
        flex-direction: column;
        /*min-height: 100vh;*/
    }

    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 64rem;
        margin: 0 auto;
        box-sizing: border-box;
    }

    footer {
        display: flex;
        justify-content: space-between;
        position: relative;
    }

    .corner {
        border: solid rgb(0, 0, 0, 0) 3px;
        border-top: white;
        border-radius: 2em;
        position: fixed;
        bottom: 10px;
        left: 10px;
        width: 3em;
        height: 3em;
    }

    .corner a {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .corner:hover {
        animation: spin 1s;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
