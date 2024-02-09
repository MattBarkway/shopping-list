<script lang="ts">
  import ListItem from "./ListItem.svelte";
  import List from "./List.svelte";
  import moment from 'moment';

  interface iList {
    id: string,
    name: string,
    owner: string,
    last_updated: string,
  }

  export let lists: iList[];
  export let sharedLists: iList[] = [];
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
      <span class="text-box narrow darker">Updated {moment(list.last_updated).fromNow()}</span>
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

<List>
  <ListItem>
    <div class="big text-box">
      👬 Shared with you
    </div>
  </ListItem>
  {#each sharedLists as list}
    <ListItem>
      <a class="text-box" href="lists/{list.id}">{list.name}</a>
      <span class="text-box">owner: {list.owner}</span>
      <span class="text-box darker">Updated {moment(list.last_updated).fromNow()}</span>
    </ListItem>
  {:else}
    <ListItem>
      <span class="text-box">
        Nobody has shared a list with you yet :'(
      </span>
    </ListItem>
  {/each}
</List>

<style>
    a {
        color: white;
    }

    .big {
        font-size: larger;
    }

    .narrow {
        width: 10%;
    }

    .darker {
        color: #999999;
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
