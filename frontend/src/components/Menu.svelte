<script lang="ts">
  import { fly, scale } from "svelte/transition";
  import { quadOut } from "svelte/easing";

  export let open = true;
  export let ready = true;

  let status1 = true;
  let status2 = true;
  export let menuItems: string[] = [];
</script>

{#if open}
  <div>
    {#each menuItems as link, i}
      <p
        transition:fly={{ y: -15, delay: 15 * i }}
        on:introstart="{() => {status1 = false; ready = false;}}"
        on:outroend="{() => {
                        status1 = true;
                        if (status1 && status2) { ready = true}
                    }}"
      >
        {link}
      </p>
    {/each}
  </div>

  <hr transition:scale={{ duration: 200, easing: quadOut, opacity: 1 }}
      on:outroend="{() => {
            status2 = true;
            if (status1 && status2) { ready = true}
        }}"
      on:introstart="{() => {status2 = false; ready = false;}}"
  />
{/if}

<style>
    :global(html) {
        background: #1d1d2f;
    }

    div {
        text-align: center;
        font-size: 1.5em;
        letter-spacing: 0.15em;
        padding: 0 1em 1em;
        color: #eeeeff;
    }

    p {
        cursor: pointer;
        width: max-content;
        margin: 1rem auto;
    }

    p:hover {
        text-decoration: underline;
        opacity: 0.7;
        transition: 0.3s;
    }
</style>
