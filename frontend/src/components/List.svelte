<script>
</script>

<div class="shopping-list">
  <slot />
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
