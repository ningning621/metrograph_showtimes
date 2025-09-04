<script lang="ts">
	import md from '$lib/utils/md';

	let { data } = $props();
</script>

<main>
	<article class="content-well">
		{@html md(data.body)}
	</article>
</main>
