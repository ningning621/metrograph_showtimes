<script>
	/** @type {String|undefined} [class="w-full bg-red"] - classes to apply to the grid container */

	/**
	 * @typedef {Object} Props
	 * @property {any} [class]
	 * @property {String} [style]
	 * @property {Number} [cols]
	 * @property {Number} [rows]
	 * @property {String} [gap]
	 * @property {String} [placeItems]
	 * @property {import('svelte').Snippet} [children]
	 */

	/** @type {Props} */
	let {
		class: classes = undefined,
		style = undefined,
		cols = 1,
		rows = 'auto',
		gap = undefined,
		placeItems = undefined,
		children
	} = $props();
</script>

<div
	class={classes}
	{style}
	style:grid-template-columns="repeat({cols}, minmax(0, 1fr))"
	style:grid-template-rows="repeat({rows}, minmax(0, 1fr))"
	style:gap
	style:place-items={placeItems}
>
	{@render children?.()}
</div>

<style lang="postcss">
	div {
		display: grid;
	}
</style>
