<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let name:string;
  export let totalItems:string;
  export let owner:string;

  export let listID:number;


  const dispatch = createEventDispatcher();
  function handleClick() {
    dispatch('click', {listID, owner});
  }

</script>

<div class="shopping-list-item" on:click={handleClick}>
    <div class="item-text">
      {name} - {totalItems} items - Owned by: {owner}
    </div>
    <div class="action"> 🗑️️</div>
</div>

<style>
    .shopping-list-item {
        display: flex;
		border-top: 1px solid rgba(0, 0, 0, 0.1);
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
		margin: 1rem 0;
        background: #252525;
        border-radius: 1em;
        color: white;
	}

    .item-text {
        width: 100%;
        padding: 1em;

    }

    .action {
        border: 1px solid #252525;
        border-radius: 1em;
        padding: 0.7em;
        margin: 0.3em;
        cursor: pointer;
    }

    .action:hover {
          background-color: #131313;
          opacity: 0.6;
          transition: 0.3s;
    }
</style>
