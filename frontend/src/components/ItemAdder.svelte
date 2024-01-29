<script>
  import ListItem from "./ListItem.svelte";
</script>

<ListItem>
  <form method="POST" class="item-input">
    <input class="text-box dark" name="item" type="text" placeholder="Add an item">
    <button class="dark no-border button">➕</button>
  </form>
</ListItem>

<style>
    .item-input {
        width: 100%;
        background: #252525;
        border: none;
        height: 100%;
        font-size: 20px;
        margin: 0.5em;
        border-radius: 0.5em;
    }

    .dark {
        background: #252525;
        color: #ffffff;
    }

    .button {
        cursor: pointer;
    }

    .no-border {
        border: 1px solid rgba(0, 0, 0, 0.1);
    }

    .text-box {
        width: 90%;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 0.5em;
    }

    input:focus {
        outline: none;
    }
</style>
