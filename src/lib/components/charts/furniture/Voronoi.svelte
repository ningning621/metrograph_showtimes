<!--
  @component
  Generates a voronoi layer using [d3-delauney](https://github.com/d3/d3-delauney).
 -->
<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import { uniques } from 'layercake';
	import { Delaunay } from 'd3';
	import type { Writable } from 'svelte/store';

	type DataPoint = [number, number] & { data: unknown };

	const { data, xGet, yGet, width, height } = getContext('LayerCake') as {
		data: Writable<unknown[]>;
		xGet: Writable<(d: unknown) => number>;
		yGet: Writable<(d: unknown) => number>;
		width: Writable<number>;
		height: Writable<number>;
	};

	interface Props {
		fill?: string;
		stroke?: string;
	}

	let { fill = 'transparent', stroke = 'none' }: Props = $props();

	const dispatch = createEventDispatcher();

	let points = $derived(
		$data.map((d) => {
			const point = [$xGet(d), $yGet(d)] as DataPoint;
			point.data = d;
			return point;
		})
	);

	let uniquePoints = $derived(uniques(points, (d: DataPoint) => d.join(), false));

	let voronoi = $derived(Delaunay.from(uniquePoints).voronoi([0, 0, $width, $height]));

	const mouseover = (point: DataPoint) => dispatch('mouseover', point);
	const mouseout = () => dispatch('mouseout');
</script>

<g role="presentation" class="voronoi" onmouseout={mouseout} onblur={mouseout}>
	{#each uniquePoints as point, i}
		<path
			role="presentation"
			{fill}
			{stroke}
			stroke-width="0"
			d={voronoi.renderCell(i)}
			onmouseover={() => mouseover(point)}
			onfocus={() => mouseover(point)}
		/>
	{/each}
</g>

<style lang="postcss">
	.voronoi path {
		pointer-events: all;
	}
</style>
