<!--
  @component
  Generates an SVG x-axis. This component is also configured to detect if your x-scale is an ordinal scale. If so, it will place the markers in the middle of the bandwidth.
 -->
<script>
	import { getContext } from 'svelte';
	const { width, height, xScale, yRange } = getContext('LayerCake');

	/**
	 * @typedef {Object} Props
	 * @property {Boolean} [gridlines]
	 * @property {Boolean} [tickMarks]
	 * @property {Boolean} [baseline]
	 * @property {Boolean} [snapTicks]
	 * @property {Function} [formatTick]
	 * @property {Number|Array|Function} [ticks]
	 * @property {Number} [xTick]
	 * @property {Number} [yTick]
	 */

	/** @type {Props} */
	let {
		gridlines = true,
		tickMarks = false,
		baseline = false,
		snapTicks = false,
		formatTick = (d) => d,
		ticks = undefined,
		xTick = 0,
		yTick = 16
	} = $props();

	let isBandwidth = $derived(typeof $xScale.bandwidth === 'function');

	let tickVals = $derived(
		Array.isArray(ticks)
			? ticks
			: isBandwidth
				? $xScale.domain()
				: typeof ticks === 'function'
					? ticks($xScale.ticks())
					: $xScale.ticks(ticks)
	);

	function textAnchor(i) {
		if (snapTicks === true) {
			if (i === 0) {
				return 'start';
			}
			if (i === tickVals.length - 1) {
				return 'end';
			}
		}
		return 'middle';
	}
</script>

<g class="axis x-axis" class:snapTicks>
	{#each tickVals as tick, i}
		<g class="tick tick-{i}" transform="translate({$xScale(tick)},{$yRange[0]})">
			{#if gridlines !== false}
				<line class="gridline" y1={$height * -1} y2="0" x1="0" x2="0" />
			{/if}
			{#if tickMarks === true}
				<line
					class="tick-mark"
					y1={0}
					y2={6}
					x1={xTick || isBandwidth ? $xScale.bandwidth() / 2 : 0}
					x2={xTick || isBandwidth ? $xScale.bandwidth() / 2 : 0}
				/>
			{/if}
			<text
				x={xTick || isBandwidth ? $xScale.bandwidth() / 2 : 0}
				y={yTick}
				dx=""
				dy=""
				text-anchor={textAnchor(i)}>{formatTick(tick)}</text
			>
		</g>
	{/each}
	{#if baseline === true}
		<line class="baseline" y1={$height + 0.5} y2={$height + 0.5} x1="0" x2={$width} />
	{/if}
</g>

<style lang="postcss">
	.tick {
		font-size: var(--textFontSize, 0.725em);
		font-weight: var(--textFontWeight, 200);
	}

	line,
	.tick line {
		stroke: var(--lineStroke, #aaa);
		stroke-dasharray: var(--lineStrokeDashArray, 2);
	}

	.tick text {
		fill: var(--textFill, #323232);
	}

	.tick .tick-mark,
	.baseline {
		stroke-dasharray: var(--baselineStrokeDashArray, 0);
	}

	.axis.snapTicks .tick:last-child text {
		transform: translateX(var(--lastTickOffset, 3px));
	}
	.axis.snapTicks .tick.tick-0 text {
		transform: translateX(var(--firstTickOffset, -3px));
	}
</style>
