<script module lang="ts">
	import type { SwiperContainer } from 'swiper/element';
	import { register } from 'swiper/element/bundle';
	register();
</script>

<script lang="ts">
	import { onMount } from 'svelte';

	type Slide = $$Generic;

	interface Props {
		slides: Slide[];
		navigation?: boolean;
		slideClass?: string;
		class?: string;
		children?: import('svelte').Snippet;
		slideSlot?: import('svelte').Snippet<[{ slide: Slide; index: number }]>;
	}

	let {
		slides,
		navigation = true,
		slideClass = '',
		class: classes = '',
		children,
		slideSlot
	}: Props = $props();

	let mounted = $state(false);
	let swiperEl: SwiperContainer | undefined = $state();

	onMount(() => {
		mounted = true;
		if (!swiperEl) return;
		Object.assign(swiperEl, {
			injectStyles: [
				`
			.swiper-button-next,
			.swiper-button-prev {
				background-color: var(--colors-foreground);
				padding: 4px 2px;
				border-radius: 50%;
				width: 24px;
				height: 24px;
			}
			.swiper-button-next {
				padding-left: 6px;
			}
			.swiper-button-prev {
				padding-right: 6px;
			}
			.swiper-button-disabled {
				display: none;
			}
			`
			]
		});

		swiperEl.initialize();
	});
</script>

<div
	class:opacity-0={!mounted}
	class="relative overflow-hidden pb-8 transition-opacity duration-300"
>
	{@render children?.()}
	<swiper-container
		bind:this={swiperEl}
		init="false"
		class="w-full !overflow-visible {classes}"
		slides-per-view="auto"
		grab-cursor="true"
		pagination-clickable="true"
		keyboard="true"
		{navigation}
		mousewheel-force-to-axis="true"
		a11y="true"
		style="
				--swiper-theme-color: {colors.foreground};
				--swiper-pagination-bullet-inactive-color: {colors.background};
				--swiper-pagination-bullet-inactive-opacity: 1;
				--swiper-navigation-size: 20px;
				--swiper-navigation-color: white;
				--swiper-navigation-top-offset: calc(50% - 20px);
				--swiper-navigation-sides-offset: 10px;
			"
	>
		{#each slides as slide, index}
			<swiper-slide class="h-auto !w-fit py-2 pr-7 pl-2 last-of-type:pr-2 {slideClass}">
				{@render slideSlot?.({ slide, index })}
			</swiper-slide>
		{/each}
	</swiper-container>
</div>

<style lang="postcss">
	:global {
		swiper-container {
			font-size: 16px;
			position: static;
		}
	}
</style>
