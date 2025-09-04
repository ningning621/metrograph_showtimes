<!--
	@component
	Zoomable treemap generator based on https://observablehq.com/@d3/treemap. Currently only takes hierarchial data.
 -->
<script lang="ts">
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { descending, hierarchy, scaleLinear, treemap, treemapSliceDice } from 'd3';

	interface Props {
		data?: any;
		height?: number;
		value?: any;
		label?: any;
		tile?: any;
		paddingOuter?: number;
		paddingInner?: number;
		fill?: string;
		strokeLineJoin?: string;
		rectCornerRadius?: number;
		rectClasses?: string;
		showLabel?: boolean;
	}

	let {
		data = [],
		height = 300,
		value = (d) => d.value,
		label = (d) => d.id,
		tile = treemapSliceDice,
		paddingOuter = 0,
		paddingInner = 0,
		fill = '#234C5E',
		strokeLineJoin = 'round',
		rectCornerRadius = 5,
		rectClasses = '',
		showLabel = true
	}: Props = $props();

	// If id and parentId options are specified, or the path option, use d3.stratify to convert tabular data to a hierarchy; otherwise we assume that the data is specified as an object {children} with nested objects (a.k.a. the 'flare.json' format), and use d3.hierarchy.
	const root = hierarchy(data)
		.sum((d) => value(d))
		.sort((a, b) => descending(value(a), value(b)));

	// calculate treemap on root
	treemap().tile(tile).paddingInner(paddingInner).paddingOuter(paddingOuter).round(false)(root);

	let width = $state(500);
	let selected = $state(root);

	const breadcrumbs = (node) => {
		const crumbs = [];
		while (node) {
			crumbs.unshift(label(node.data));
			node = node.parent;
		}
		return crumbs.join('/');
	};

	const select = (node) => {
		while (node.parent && node.parent !== selected) node = node.parent;
		if (node && node.children) selected = node;
	};

	const extents = tweened(undefined, {
		easing: cubicOut,
		duration: 300
	});

	$effect(() => {
		$extents = {
			x0: selected.x0,
			x1: selected.x1,
			y0: selected.y0,
			y1: selected.y1
		};
	});

	let xScale = $derived(scaleLinear().domain([$extents.x0, $extents.x1]).range([0, width]));

	let yScale = $derived(scaleLinear().domain([$extents.y0, $extents.y1]).range([0, height]));

	// select children nodes but also keep the sibling nodes of the selected layer to keep object permanence.
	let nodes = $derived(
		[
			selected.children,
			selected === root ? [] : selected.parent ? selected.parent.children : root.children
		]
			.flat()
			.filter((node) => node !== selected)
	);
</script>

<button
	class="group w-full cursor-pointer text-left disabled:cursor-not-allowed"
	disabled={selected === root}
	onclick={() => (selected = selected.parent)}
>
	<i
		class="fas fa-arrow-left translate-x-0.5 align-middle text-xs font-thin transition-all duration-300 ease-out group-hover:-translate-x-0"
		class:opacity-0={selected === root}
		class:w-0={selected === root}
		class:w-3={selected !== root}
	></i>
	<span class="align-middle">{breadcrumbs(selected)}</span>
</button>

<div class="w-full" style:height="{height}px" bind:clientWidth={width}>
	<svg class="h-full w-full overflow-hidden">
		{#each nodes as node (node)}
			{@const x = xScale(node.x0)}
			{@const y = yScale(node.y0)}
			{@const w = xScale(node.x1) - xScale(node.x0)}
			{@const h = yScale(node.y1) - yScale(node.y0)}

			<g class="overflow-clip" transform="translate({x},{y})">
				<rect
					role="presentation"
					width={w}
					height={h}
					{fill}
					stroke-linejoin={strokeLineJoin}
					rx={rectCornerRadius}
					ry={rectCornerRadius}
					class={rectClasses}
					class:cursor-not-allowed={!node.children}
					class:cursor-pointer={node.children}
					onclick={() => select(node)}
					onfocus={() => select(node)}
					onkeydown={(e) => {
						if (e.key !== 'Enter') return;
						select(node);
					}}
				/>
				<title>{label(node.data)}</title>
				{#if showLabel}
					<text class="text-xs" y="14px" x="8px">{label(node.data)}</text>
				{/if}
			</g>
		{/each}
	</svg>
</div>
