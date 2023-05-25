<script lang="ts">
	import { spring } from 'svelte/motion';
    import ShoppingListItem from "./ShoppingListItem.svelte";
    import ItemAdder from "./ItemAdder.svelte";

    let count = 43;

	const displayed_count = spring();
	$: displayed_count.set(count);
	$: offset = modulo($displayed_count, 1);

	function modulo(n: number, m: number) {
		// handle negative numbers
		return ((n % m) + m) % m;
	}
</script>

<div class="shopping-list">
    <ItemAdder />
    <ShoppingListItem />
    <ShoppingListItem />
    <ShoppingListItem />
    <ShoppingListItem />
    <ShoppingListItem />
    <ShoppingListItem />

</div>

<style>
    * {
        font-family: Helvetica, sans-serif;
    }

	.shopping-list {
        font-family: Helvetica, sans-serif;
		border-top: 1px solid rgba(0, 0, 0, 0.1);
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
		margin: 1rem 0;
        padding: 1rem;
        background: #444444;
        border-radius: 1em;
        opacity: 0.5;
        color: white;
	}
</style>
