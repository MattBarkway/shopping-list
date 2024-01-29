<script lang="ts">
  import type { PageData } from "./$types";
  import ShoppingList from "../../../components/ShoppingList.svelte";
  import { page } from "$app/stores";

  export let data: PageData;

  async function handleItemEdit(event: any) {
    console.log("top edit item event:", event.detail);
    await fetch(`/lists/${$page.params.listID}`, {
      method:'POST',
      body: JSON.stringify({event})
    })
  }

  async function handleItemDelete(event: any) {
    console.log("top delete item event:", event.detail);
  }
</script>

<svelte:head>
  <title>{data.list.name}</title>
</svelte:head>
<h1> {data.list.name} </h1>
<ShoppingList
  items="{data.items}"
  on:edit-item={handleItemEdit}
  on:delete-item={handleItemDelete}
/>
