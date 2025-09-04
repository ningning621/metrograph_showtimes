<script lang="ts">
	import '$lib/styles/app.css';
	import 'iconify-icon';
	import { Toaster } from 'svelte-french-toast';

	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

{@render children?.()}

<Toaster />
