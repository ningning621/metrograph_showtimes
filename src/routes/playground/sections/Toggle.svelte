<script lang="ts">
	import Toggle from '$lib/components/interactivity/Toggle.svelte';

	const items = ['Bar Chart', 'Line Chart', 'Scatterplot', 'Dot Plot'];

	let value1 = $state(items[0]);
	let value2 = $state([items[0]]);
</script>

<div
	class="border-tertiary flex w-full flex-row flex-wrap items-center justify-around gap-2 gap-y-6 rounded-sm border border-dashed p-8"
>
	<div class="flex flex-col gap-2">
		<p class="font-medium">Toggle Group - Single</p>
		<Toggle {items} bind:value={value1} />
		<p><span class="font-medium">Selected:</span> {value1}</p>
	</div>

	<div class="flex flex-col gap-2">
		<p class="font-medium">Toggle Group - Multi-Select</p>
		<Toggle {items} bind:value={value2} type="multiple" />
		<p><span class="font-medium">Selected:</span> {value2}</p>
	</div>
</div>
