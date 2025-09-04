<script lang="ts">
	// TODO: give data props to pass to tie in values to paths
	// TODO: generalize design + classes to pass
	import { geoAlbersUsa, geoPath } from 'd3';
	import { feature } from 'topojson-client';
	import { raise } from 'layercake';
	import topojson from '$lib/data/cartography/states.topojson.json';

	let containerWidth = $state(300);
	const heightWidthProportion = 0.585;
	const viewboxDims: [number, number] = [960, 960 * heightWidthProportion];

	const geojson = feature(topojson, topojson.objects.collection);
	const projectionFn = geoAlbersUsa().fitSize(viewboxDims, geojson);
	const geoPathFn = geoPath(projectionFn);

	const raiseFeature = (e: Event) => {
		raise(e.target as HTMLElement);
	};
</script>

<div
	class="w-full"
	style:height="{containerWidth * heightWidthProportion}px"
	bind:clientWidth={containerWidth}
>
	<svg
		class="viz-container mx-auto h-full w-full overflow-visible"
		viewBox="0 0 {viewboxDims[0]} {viewboxDims[1]}"
	>
		<g>
			{#each geojson.features as feature}
				<path
					role="presentation"
					class="hover: stroke-1"
					d={geoPathFn(feature)}
					onmouseover={raiseFeature}
					onfocus={raiseFeature}
					onkeydown={(e) => {
						if (e.key === 'Enter') {
							raiseFeature(e);
						}
					}}
				>
					<title>{feature.properties.name}</title>
				</path>
			{/each}
		</g>
	</svg>
</div>
