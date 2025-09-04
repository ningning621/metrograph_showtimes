<script>
	import md from '$lib/utils/md';

	let { data } = $props();
</script>

{#if data?.body}
	<div class="content-well">
		{@html md(data?.body || '')}
	</div>
{/if}
