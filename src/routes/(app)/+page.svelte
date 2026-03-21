<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';
	import films from '$lib/data/films.csv';
	import meta from '$lib/data/meta.json';
	import Floating from '$lib/components/interactivity/Floating.svelte';

	const lastUpdated = meta.lastUpdated
		? (() => {
				const d = new Date(meta.lastUpdated);
				const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
				const dd = String(d.getUTCDate()).padStart(2, '0');
				const yyyy = d.getUTCFullYear();
				return `${mm}.${dd}.${yyyy}`;
			})()
		: '';

	onMount(() => {
		const tl = gsap.timeline();

		tl.from('[data-header-item]', {
			opacity: 0,
			y: 8,
			duration: 0.5,
			ease: 'power2.out',
			stagger: 0.12
		})
			.from('[showAfterHeader]', { opacity: 0, y: 6, duration: 0.35, ease: 'power2.out' }, '-=0.05')
			.from(
				'[data-table-row]',
				{
					opacity: 0,
					y: 6,
					duration: 0.35,
					ease: 'power2.out',
					stagger: 0.04
				},
				'<'
			);
	});

	const parseDirectors = (directorsStr: string) => {
		if (!directorsStr) return '';
		// Match either "double-quoted" or 'single-quoted' names, handling apostrophes inside names
		const matches = [...directorsStr.matchAll(/"([^"]+)"|'([^']+)'/g)];
		if (matches.length > 0) {
			return matches.map((m) => m[1] ?? m[2]).join(', ');
		}
		return directorsStr;
	};

	let tooltip = $state(null);
</script>

<svelte:window onscroll={() => (tooltip = null)} />

<div class="text-dark-cobalt w-full px-6 py-6 md:w-[62%] md:px-12">
	<header class=" mb-8 flex w-full flex-col gap-2">
		<h1
			data-header-item
			class="font-display text-2xl font-bold tracking-[90%] uppercase md:tracking-[100%]"
		>
			Metrograph Weekly
		</h1>
		<div class="flex flex-col gap-px">
			<p data-header-item class="text-sm">
				The weekly film schedule at
				<a class="underline" href="https://metrograph.com" target="_blank"> Metrograph </a> (in NY),
				ranked by Letterboxd rating.
			</p>
			<p data-header-item class="font-sans text-xs font-light uppercase">
				Last Updated {lastUpdated}
			</p>
		</div>
	</header>

	<section class="relative flex flex-row gap-2">
		<table showAfterHeader class="table">
			<thead>
				<tr class="font-display text-xs">
					<th class="px-2 pb-4 font-normal"></th>
					<th class="pr-2 pb-4 font-normal"></th>
					<th class="pr-4 pb-4 text-left font-normal">Title</th>
					<th class="hidden px-2 pb-4 text-left font-normal md:block">Directors</th>
					<th class="px-2 pb-4 font-normal">↓</th>
				</tr>
			</thead>
			<tbody>
				{#each films.sort((a, b) => b.rating - a.rating) as film}
					<tr
						data-table-row
						class="border-border/50 text-light hover:bg-cobalt cursor-pointer border-b text-sm transition-colors duration-150 hover:text-white"
						onclick={() => window.open(film.letterboxd_url, '_blank')}
						onmouseenter={() => (tooltip = film)}
						onmouseleave={() => (tooltip = null)}
					>
						<td class="px-2 py-2 text-center align-top">{film.event_time_date ? '🗓️' : ''}</td>
						<td class="py-2 pr-2 align-top">
							<img src={film.imageUrl} alt={film.title} class="aspect-video w-8 min-w-8" />
						</td>
						<td class="py-2 pr-4 align-top uppercase">
							<p>
								{film.title}
							</p>

							<p class="text-normal block text-[10px] md:hidden">
								{parseDirectors(film.directors)}
							</p>
						</td>
						<td class="hidden px-2 py-2 align-top uppercase md:block"
							>{parseDirectors(film.directors)}</td
						>
						<td class="px-2 py-2 align-top">{film.rating.toFixed(1)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
		<p
			showAfterHeader
			class="font-display self-start pt-11 text-xs font-normal whitespace-nowrap uppercase"
			style="writing-mode: vertical-rl;"
		>
			Letterboxd Rating
		</p>
	</section>
</div>

{#if tooltip}
	<Floating>
		<p class="text-xs">See the film on Letterboxd</p>
	</Floating>
{/if}
