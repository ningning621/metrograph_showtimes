<!--
	@component
	Static treemap generator based on https://observablehq.com/@d3/treemap
 -->
<script lang="ts">
	import {
		InternSet,
		descending,
		hierarchy,
		scaleLinear,
		scaleOrdinal,
		stratify,
		treemap,
		treemapSliceDice
	} from 'd3';

	interface Props {
		data?: any;
		height?: number;
		path?: any;
		id?: any;
		parentId?: any;
		value?: any;
		label?: any;
		group?: any;
		zDomain?: any;
		colors?: any;
		fill?: string;
		tile?: any;
		paddingOuter?: number;
		paddingInner?: number;
		strokeLineJoin?: string;
		showLabel?: boolean;
		rectCornerRadius?: number;
		rectClasses?: string;
	}

	let {
		data = [],
		height = 300,
		path = null,
		id = Array.isArray(data) ? (d) => d.id : null,
		parentId = Array.isArray(data) ? (d) => d.parentId : null,
		value = (d) => d.value,
		label = (d) => d.name,
		group = null,
		zDomain = $bindable(null),
		colors = ['#234C5E', '#00CCB3', '#fcd34d', '#fef3c7'],
		fill = '#234C5E',
		tile = treemapSliceDice,
		paddingOuter = 0,
		paddingInner = 0,
		strokeLineJoin = 'round',
		showLabel = true,
		rectCornerRadius = 0,
		rectClasses = ''
	}: Props = $props();

	// If id and parentId options are specified, or the path option, use d3.stratify to convert tabular data to a hierarchy; otherwise we assume that the data is specified as an object {children} with nested objects (a.k.a. the 'flare.json' format), and use d3.hierarchy.
	const root =
		path != null
			? stratify().path(path)(data)
			: id != null || parentId != null
				? stratify().id(id).parentId(parentId)(data)
				: hierarchy(data)
						.sum((d) => value(d))
						.sort((a, b) => descending(value(a), value(b)));

	// Compute the values of internal nodes by aggregating from the leaves.
	value == null ? root.count() : root.sum((d) => Math.max(0, value(d)));

	const leaves = root.leaves();

	const G = group == null ? null : leaves.map((d) => group(d.data, d));
	if (zDomain === undefined) zDomain = G;
	zDomain = new InternSet(zDomain);
	const color = group == null ? null : scaleOrdinal(zDomain, colors);

	// calculate treemap on root
	treemap().tile(tile).paddingInner(paddingInner).paddingOuter(paddingOuter).round(false)(root);

	let width = $state(500);

	let xScale = $derived(scaleLinear().domain([0, 1]).range([0, width]));

	let yScale = $derived(scaleLinear().domain([0, 1]).range([0, height]));
</script>

<div class="w-full" style:height="{height}px" bind:clientWidth={width}>
	<svg class="h-full w-full overflow-hidden">
		{#each leaves as node, i (node)}
			{@const x = xScale(node.x0)}
			{@const y = yScale(node.y0)}
			{@const w = xScale(node.x1) - xScale(node.x0)}
			{@const h = yScale(node.y1) - yScale(node.y0)}
			<g transform="translate({x},{y})">
				<rect
					width={w}
					height={h}
					fill={color ? color(G[i]) : fill}
					stroke-linejoin={strokeLineJoin}
					class={rectClasses}
					rx={rectCornerRadius}
					ry={rectCornerRadius}
				/>
				<title>{label(node.data)}</title>
				{#if showLabel}
					<text class="text-xs" y="14px" x="8px">{label(node.data)}</text>
				{/if}
			</g>
		{/each}
	</svg>
</div>
