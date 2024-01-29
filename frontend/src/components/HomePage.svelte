<script lang="ts">
  import ListItem from "./ListItem.svelte";
  import List from "./List.svelte";

  interface iList {
    id: string,
    name: string,
  }

  export let lists: iList[];
</script>

<List>
  <ListItem>
    <div class="big text-box">
      📝 Your lists
    </div>
  </ListItem>
  {#each lists as list}
    <ListItem>
      <a class="text-box" href="lists/{list.id}">{list.name}</a>
    </ListItem>
  {:else}
    <ListItem>
      <span class="text-box">
        You don't have any lists :( create one <a href="lists/new">here</a>
      </span>
    </ListItem>
  {/each}
  <ListItem><a class="text-box" href="lists/new">create a new list</a></ListItem>
</List>

<style>
    a {
        color: white;
    }

    .big {
        font-size: larger;
    }

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
