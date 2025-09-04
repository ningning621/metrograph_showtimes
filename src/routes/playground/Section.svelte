<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		id: string;
		title: string;
		description: string;
		children: Snippet;
	}

	let { id, title, description, children }: Props = $props();
</script>

<section {id} class="content-well scroll-mt-24">
	<!-- Section Header -->
	<div class="mb-8">
		<h2 class="headline-2 text-primary mb-3 font-bold">{title}</h2>
		<p class="body-1 text-secondary max-w-3xl leading-relaxed">{description}</p>
	</div>

	<!-- Content Area -->
	<div class="bg-primary border-primary rounded-lg border p-8 shadow-sm">
		{@render children()}
	</div>
</section>
