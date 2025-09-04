<script lang="ts">
	import md from '$lib/utils/md';

	let { data } = $props();
</script>

<div class="content-well">
	<header class="full bg-secondary mb-8 grid min-h-[60vh] place-content-center">
		<h1 class="text-6xl font-bold">{data.title}</h1>
	</header>

	<section>
		{@html md(data.body)}
	</section>
</div>
