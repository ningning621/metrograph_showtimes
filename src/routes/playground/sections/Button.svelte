<script lang="ts">
	import Button from '$lib/components/interactivity/Button.svelte';

	let clicked = $state(false);
</script>

<div class="flex flex-row flex-wrap items-center gap-2">
	<Button size="sm" color="primary" variant="pill" icon="arrow-right" href="https://www.google.com"
		>Button</Button
	>
	<Button size="md" color="primary" variant="pill" icon="arrow-right" href="#">Button</Button>
	<Button
		size="lg"
		color="primary"
		variant="pill"
		icon="arrow-right"
		onclick={() => (clicked = true)}
		disabled={clicked}>Button</Button
	>
	<Button size="sm" color="accent" variant="pill" icon="arrow-right">Button</Button>
	<Button size="md" color="accent" variant="pill" icon="arrow-right">Button</Button>
	<Button size="lg" color="accent" variant="pill" icon="arrow-right">Button</Button>
	<Button size="sm" color="primary" variant="underlined" icon="arrow-right">Button</Button>
	<Button size="md" color="primary" variant="underlined" icon="arrow-right">Button</Button>
	<Button size="lg" color="primary" variant="underlined" icon="arrow-right">Button</Button>
	<Button size="sm" color="accent" variant="underlined" icon="arrow-right">Button</Button>
	<Button size="md" color="accent" variant="underlined" icon="arrow-right">Button</Button>
	<Button size="lg" color="accent" variant="underlined" icon="arrow-right">Button</Button>
</div>
