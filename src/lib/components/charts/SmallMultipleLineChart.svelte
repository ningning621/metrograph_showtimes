<script lang="ts">
	import { LayerCake, Svg } from 'layercake';
	import weather from '$lib/data/weather.csv';

	import { format, groups, scaleTime, timeParse } from 'd3';
	import { apmonth } from 'journalize';

	import Line from '$lib/components/charts/furniture/Line.svelte';
	import Voronoi from '$lib/components/charts/furniture/Voronoi.svelte';
	import AxisX from '$lib/components/charts/furniture/AxisX.svelte';
	import AxisY from '$lib/components/charts/furniture/AxisY.svelte';
	import Floating from '$lib/components/interactivity/Floating.svelte';

	interface Props {
		height?: string;
	}

	let { height = '400px' }: Props = $props();

	let tooltip = $state();
	let parentContainer = $state();

	const grouped = groups(weather, (d) => d.variable);
</script>

<div class="grid grid-cols-3 gap-8" bind:this={parentContainer}>
	{#each grouped as [variable, data]}
		<figure class="m-0">
			<figcaption class="m-0">{variable}</figcaption>
			<div class="w-full" style:height>
				<LayerCake
					padding={{ left: 0, bottom: 0, right: 0, top: 20 }}
					x={(d) => timeParse('%B')(d.month)}
					y="value"
					xScale={scaleTime()}
					{data}
				>
					<Svg>
						<g>
							<AxisX
								baseline
								gridlines={false}
								snapTicks
								ticks={[
									timeParse('%B')('January'),
									timeParse('%B')('June'),
									timeParse('%B')('December')
								]}
								formatTick={(tick) => apmonth(tick)}
							/>
							<AxisY />
						</g>

						<Line hasArea class="" areaClass="opacity-20" strokeWidth="3" strokeLineCap="round" />

						{#if tooltip && tooltip.detail.data.variable === variable}
							<line
								x1={tooltip.detail[0]}
								x2={tooltip.detail[0]}
								y1="80"
								y2="0"
								stroke="black"
								stroke-width="2"
								mix-blend-mode="multiply"
							/>
						{/if}

						<Voronoi
							on:mouseover={(e) => (tooltip = e)}
							on:mouseout={() => (tooltip = undefined)}
						/>
					</Svg>
				</LayerCake>
			</div>
		</figure>
	{/each}
	{#if !!tooltip}
		<Floating>
			<p class="my-0 text-xs">
				{tooltip.detail.data.month}'s {tooltip.detail.data.variable} was {format('.2f')(
					tooltip.detail.data.value
				)}
			</p>
		</Floating>
	{/if}
</div>
