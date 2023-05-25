<script>
    import {fly, scale} from 'svelte/transition';
    import {quadOut} from 'svelte/easing';

    export let open;
    export let ready = true;

    let status1;
    let status2;
</script>

{#if open}
    <div>
        {#each ['Home', 'Example', 'About', 'Contact'] as link, i}
            <p
                    transition:fly={{ y: -15, delay: 50 * i }}
                    on:introstart="{() => {status1 = false; ready = false;}}"
                    on:outroend="{() => {
                        status1 = true;
                        if (status1 && status2) { ready = true}
                    }}"
            >
                {link}
            </p>
        {/each}
    </div>

    <hr transition:scale={{ duration: 750, easing: quadOut, opacity: 1 }}
        on:outroend="{() => {
            status2 = true;
            if (status1 && status2) { ready = true}
        }}"
        on:introstart="{() => {status2 = false; ready = false;}}"
    />
{/if}

<style>
    :global(html) {
        background: #1d1d2f;
    }

    div {
        text-align: center;
        font-size: 1.5em;
        letter-spacing: 0.15em;
        padding: 1em;
        padding-top: 0;
        color: #eef;
    }

    p {
        cursor: pointer;
        width: max-content;
        margin: 1rem auto;
    }

    p:hover {
        text-decoration: underline;
    }
</style>