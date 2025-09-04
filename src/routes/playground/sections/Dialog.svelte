<script lang="ts">
	import Dialog from '$lib/components/interactivity/Dialog.svelte';
</script>

<div class="border-tertiary flex w-full flex-row flex-wrap items-center justify-center gap-2">
	<Dialog title="Centered Dialog Title" description="Dialog Description">
		{#snippet trigger()}
			<div class="button md pill primary">Open Centered Dialog</div>
		{/snippet}
		{#snippet content()}
			Dialog Content
		{/snippet}
	</Dialog>
	<Dialog title="Left Dialog Title" description="Dialog Description" placement="left">
		{#snippet trigger()}
			<div class="button md pill primary">Open Left Dialog</div>
		{/snippet}
		{#snippet content()}
			Dialog Content
		{/snippet}
	</Dialog>
	<Dialog title="Right Dialog Title" description="Dialog Description" placement="right">
		{#snippet trigger()}
			<div class="button md pill primary">Open Right Dialog</div>
		{/snippet}
		{#snippet content()}
			Dialog Content
		{/snippet}
	</Dialog>
</div>
