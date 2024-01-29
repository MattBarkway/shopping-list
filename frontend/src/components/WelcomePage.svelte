<script lang="ts">
  import ListItem from "./ListItem.svelte";
  import List from "./List.svelte";
</script>

<List>
  <ListItem>
    <p class="big item-text">
      📝 Welcome to Lists
    </p>
  </ListItem>
  <ListItem>
    <span class="item-text">
      Get started by
      <a href="/login">signing in</a> or
      <a href="/register">registering</a>.
    </span>
  </ListItem>
</List>


<style>
    .big {
        font-size: larger;
    }
    a {
        color: #a8a8a8;
    }

    .item-text {
        width: 100%;
        padding: 1em;
    }
</style>
