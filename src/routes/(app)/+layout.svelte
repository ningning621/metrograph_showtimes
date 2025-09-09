<script lang="ts">
	import Head from '$lib/components/furniture/Head.svelte';
	import Masthead from '$lib/components/furniture/Masthead.svelte';
	import Colophon from '$lib/components/furniture/Colophon.svelte';

	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<Head />

<!-- <Masthead /> -->

<!-- #main-content is the skip-to link for the masthead. Apply it here or on another element, but it MUST exist somewhere -->
<main id="main-content" class="flex-1">
	{@render children?.()}
</main>

<!-- <Colophon /> -->

<!-- {#if ReloadPrompt}
	<svelte:component this={ReloadPrompt} />
{/if} -->
