<script lang="ts">
  import List from "./List.svelte";
  import ListItem from "./ListItem.svelte";

  export let submitText: string;
</script>

<form method="POST">
  <List>
    <ListItem>
      <input class="text-box dark" name="email" type="email" placeholder="email">
    </ListItem>
    <ListItem>
      <input class="text-box dark" name="password" type="password" placeholder="password">
    </ListItem>
    <button class="dark button">{submitText}</button>
    <slot />
  </List>
</form>

<style>
    .dark {
        background: #252525;
        color: #ffffff;
    }

    .button {
        cursor: pointer;
        padding: 0.5em;
        border-radius: 0.5em;
        border: none;
    }


    .text-box {
        margin-left: 1em;
        width: 90%;
        /*border: 1px solid rgba(0, 0, 0, 0.1);*/
        padding: 0.5em;
        border: none;
    }

    input:focus {
        outline: none;
        border: none;
    }
</style>
