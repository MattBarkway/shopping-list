<script lang="ts">
  import type { PageData } from "./$types";
  import ShoppingList from "../../../components/ShoppingList.svelte";
  import { page } from "$app/stores";
  import { invalidateAll, goto } from "$app/navigation";
  import List from "../../../components/List.svelte";
  import ListItem from "../../../components/ListItem.svelte";

  export let data: PageData;

  $: collaborator = "";

  $: isShareModal = false;

  async function handleItemEdit(event: any) {
    await fetch(`/lists/${$page.params.listID}`, {
      method: "POST",
      body: JSON.stringify(event.detail)
    });
  }

  async function handleItemDelete(event: any) {
    await fetch(`/lists/${$page.params.listID}`, {
      method: "DELETE",
      body: JSON.stringify(event.detail)
    });
    await invalidateAll();
  }


  async function openSharingModal(event: any) {
    isShareModal = true;
  }

  async function addCollaborator(event: any) {
    await fetch(`/lists/${$page.params.listID}/collaborator/`, {
      method: "POST",
      body: JSON.stringify({ collaborator })
    });
    isShareModal = false;
  }
</script>

<svelte:head>
  <title>{data.list.name}</title>
</svelte:head>
<button on:click={async () => await goto('/')} class="breadcrumb">&lt;- Back to my lists</button>
{#if data.isOwner}
  <button on:click={openSharingModal} class="breadcrumb">👬Add Collaborator</button>
{/if}
{#if isShareModal}
  <List>
    <ListItem>
      <input class="text-box dark" name="email" type="email" placeholder="email" bind:value={collaborator}>
    </ListItem>
    <button class="dark button" on:click={addCollaborator}>Add</button>
  </List>
{/if}
<!--TODO: show success/error message-->

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
        margin: 0.2em;
    }
</style>
