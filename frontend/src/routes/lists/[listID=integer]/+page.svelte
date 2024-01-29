<script lang="ts">
  import type { PageData } from "./$types";
  import ShoppingList from "../../../components/ShoppingList.svelte";
  import { page } from "$app/stores";
  import { invalidateAll, goto } from "$app/navigation";
  import List from "../../../components/List.svelte";
  import ListItem from "../../../components/ListItem.svelte";

  export let data: PageData;

  $: isShareModal = false;

  async function handleItemEdit(event: any) {
    console.log("top edit item event:", event.detail);
    await fetch(`/lists/${$page.params.listID}`, {
      method: "POST",
      body: JSON.stringify(event.detail)
    });
  }

  async function handleItemDelete(event: any) {
    console.log("top delete item event:", event.detail);
    await fetch(`/lists/${$page.params.listID}`, {
      method: "DELETE",
      body: JSON.stringify(event.detail)
    });
    invalidateAll();
  }


  async function openSharingModal(event: any) {
    console.log("opening share modal!");
    isShareModal = true;
  }
</script>

<svelte:head>
  <title>{data.list.name}</title>
</svelte:head>
<button on:click={async () => await goto('/')} class="breadcrumb">&lt;- Back to my lists</button>
<button on:click={openSharingModal} class="breadcrumb">👬Add Collaborator</button>
<!--TODO add colaborators-->
{#if isShareModal}
  <form method="POST">
    <List>
      <ListItem>
        <input class="text-box dark" name="email" type="email" placeholder="email">
      </ListItem>
      <button class="dark button">Add</button>
    </List>
  </form>
{/if}

<h1> {data.list.name} </h1>
<ShoppingList
  items="{data.items}"
  on:edit-item={handleItemEdit}
  on:delete-item={handleItemDelete}
/>


<style>
    .breadcrumb {
        width: 15%;
        border: none;
        border-radius: 0.2em;
        background: #444444;
        color: white;
        padding: 0.3em;
        opacity: 0.5;
        cursor: pointer;
    }
</style>