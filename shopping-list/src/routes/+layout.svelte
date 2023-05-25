<script>
    import './styles.css';
    import github from '$lib/images/github.svg';
    import {Hamburger} from "svelte-hamburgers";
    import Menu from "./Menu.svelte";

    let open;
</script>

<Hamburger bind:open color="white" class="nav"/>
<Menu bind:open class="nav" style="position: absolute; z-index: 1000;"/>

{#if !open}
    <div class="app">
        <main>
            hello
            <slot/>
        </main>

        <footer>
            <div class="corner">
                <a href="https://github.com/mattbarkway">
                    <img src={github} alt="GitHub"/>
                </a>
            </div>
        </footer>
    </div>
{/if}

<style>
    .nav {
        position: absolute;
        z-index: 100;
        background: #444444;
        border-radius: 1em;
    }

    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 64rem;
        margin: 0 auto;
        box-sizing: border-box;
    }

    footer {
        display: flex;
        justify-content: space-between;
    }

    .corner {
        width: 3em;
        height: 3em;
    }

    .corner a {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }

    .corner img {
        width: 2em;
        height: 2em;
        object-fit: contain;
    }
</style>
