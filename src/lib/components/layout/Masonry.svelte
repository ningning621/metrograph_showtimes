<!-- inspired by https://github.com/janosh/svelte-bricks -->
<script lang="ts">
	import { flip } from 'svelte/animate';
	import { fly } from 'svelte/transition';

	type Item = any;

	interface Props {
		nCols?: number;
		width?: number;
		height?: number;
		items?: Item[];
		style?: string;
		duration?: number;
		columnClass?: string;
		class?: string;
		id: (item: Item) => string | string;
		content: import('svelte').Snippet<[number, Item]>;
	}

	let {
		nCols = 2,
		width = 0,
		height = 0,
		items = [],
		style = '',
		duration = 200,
		columnClass = '',
		class: classes = '',
		id = (item: Item) => {
			if (['string', 'number'].includes(typeof item)) return item;
			return item.id;
		},
		content
	}: Props = $props();

	let getId = (item: Item) => (typeof id === `function` ? id(item) : item[id]);

	let columns = $derived(
		items.reduce(
			(cols, item, i) => {
				cols[i % cols.length].push([item, i]);
				return cols;
			},
			Array.from({ length: nCols }, () => [])
		)
	);
</script>

<div
	class="masonry box-border flex w-full {classes}"
	{style}
	bind:clientWidth={width}
	bind:clientHeight={height}
>
	{#each columns as col}
		<div class="col grid h-max w-full {columnClass}">
			{#if duration}
				{#each col as [item, i] (getId(item))}
					<div
						in:fly={{ duration, y: -5 }}
						out:fly={{ duration, y: -5 }}
						animate:flip={{ duration }}
					>
						{@render content?.(i, item)}
					</div>
				{/each}
			{:else}
				{#each col as [item, i] (getId(item))}
					<div>
						{@render content?.(i, item)}
					</div>
				{/each}
			{/if}
		</div>
	{/each}
</div>

<style lang="postcss">
	.masonry,
	.col {
		gap: var(--gap, 12px);
	}
	.masonry {
		overflow-wrap: anywhere;
	}
	.col {
		max-width: var(--max-col-width, 100%);
	}
</style>
