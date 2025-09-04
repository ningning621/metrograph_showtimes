<script>
	import { area, curveMonotoneX, line } from 'd3';
	import { getContext } from 'svelte';

	const { data, xGet, yGet, yRange } = getContext('LayerCake');

	/** @type {string | undefined} class="stroke-teal" - classes to apply to the path */

	/**
	 * @typedef {Object} Props
	 * @property {import('d3').CurveFactory} curve={curveMonotoneX} [curve]
	 * @property {string | undefined} [stroke]
	 * @property {number} [strokeWidth]
	 * @property {string | undefined} [strokeDashArray]
	 * @property {('bevel' | 'miter' | 'round' | 'inherit') | undefined} [strokeLineJoin]
	 * @property {('butt' | 'round' | 'square') | undefined} [strokeLineCap]
	 * @property {string | undefined} [style]
	 * @property {string | undefined} [transform]
	 * @property {() => boolean} defined={() => true} [defined]
	 * @property {string | undefined} hasArea={true} [hasArea]
	 * @property {any} [class]
	 * @property {string | undefined} [areaClass]
	 */

	/** @type {Props} */
	let {
		curve = curveMonotoneX,
		stroke = undefined,
		strokeWidth = 1,
		strokeDashArray = undefined,
		strokeLineJoin = undefined,
		strokeLineCap = undefined,
		style = undefined,
		transform = undefined,
		defined = () => true,
		hasArea = undefined,
		class: classes = undefined,
		areaClass = undefined
	} = $props();
</script>

<g>
	<path
		class={classes}
		{transform}
		{stroke}
		stroke-width={strokeWidth}
		stroke-dasharray={strokeDashArray}
		stroke-linejoin={strokeLineJoin}
		stroke-linecap={strokeLineCap}
		fill="none"
		{style}
		d={line()
			.defined(defined)
			.x((d) => $xGet(d))
			.y((d) => $yGet(d))
			.curve(curve)($data)}
	/>

	{#if hasArea}
		<path
			class={areaClass}
			fill={stroke}
			stroke-width={strokeWidth}
			stroke-dasharray={strokeDashArray}
			stroke-linejoin={strokeLineJoin}
			stroke-linecap={strokeLineCap}
			opacity=".25"
			d={area()
				.defined(defined)
				.x((d) => $xGet(d))
				.y0(() => $yRange[0])
				.y1((d) => $yGet(d))
				.curve(curve)($data)}
		/>
	{/if}
</g>
