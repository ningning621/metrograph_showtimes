<script lang="ts">
	// TODO: give data props to pass to tie in values to tile
	// TODO: generalize design + classes to pass
	import states from '$lib/data/cartography/states.json';
	interface Props {
		tile?: import('svelte').Snippet;
	}

	let { tile }: Props = $props();
	const stateIdxMap = new Map(states.map((state) => [state.idx, state]));

	let size = $state(25);
</script>

<div class="grid grid-cols-11 grid-rows-[repeat(8,_minmax(0,_1fr))] gap-0.5">
	<!-- 11 * 8 small multiple cartogram -->
	{#each Array.from({ length: 11 * 8 }) as _, i}
		{@const state = stateIdxMap.get(i) || false}
		<!-- first tile that isn't filled -->
		{#if i === 1}
			<div bind:clientWidth={size} style:height="{size}px" aria-hidden="true"></div>
		{:else if state}
			<div
				class="pointer-events-auto relative flex items-center justify-center overflow-hidden rounded-sm"
				style:height="{size}px"
			>
				<span class="m-0 p-0 text-center font-sans text-sm">
					{state.postal}
				</span>
				{@render tile?.()}
			</div>
		{:else}
			<div class="pointer-events-none" style:height="{size}px" aria-hidden="true"></div>
		{/if}
	{/each}
</div>
