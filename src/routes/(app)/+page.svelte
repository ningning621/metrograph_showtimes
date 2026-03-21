<script lang="ts">
	import md from '$lib/utils/md';
	import films from '$lib/data/films.csv';
	import meta from '$lib/data/meta.json';

	const lastUpdated = meta.lastUpdated
		? (() => {
				const d = new Date(meta.lastUpdated);
				const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
				const dd = String(d.getUTCDate()).padStart(2, '0');
				const yyyy = d.getUTCFullYear();
				return `${mm}.${dd}.${yyyy}`;
			})()
		: '';

	console.log(films);

	// Helper function to parse directors string and join with comma
	function parseDirectors(directorsStr: string): string {
		try {
			// Parse the Python list string format like "['Name1', 'Name2']"
			const parsed = JSON.parse(directorsStr.replace(/'/g, '"'));
			return Array.isArray(parsed) ? parsed.join(', ') : directorsStr;
		} catch {
			return directorsStr;
		}
	}
</script>

<div class="px-6 py-6 md:px-12">
	<header class="mb-8 flex w-full flex-col gap-2">
		<h1 class="font-display text-2xl font-bold tracking-[90%] uppercase md:tracking-[100%]">
			Metrograph Weekly
		</h1>
		<p class="font-sans text-xs font-light uppercase">Last Updated {lastUpdated}</p>
	</header>

	<section class="relative flex flex-row gap-2">
		<table class="table">
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
						class="border-border/50 text-light hover:bg-cobalt/25 cursor-pointer border-b text-sm transition-colors duration-150"
						on:click={() => window.open(film.letterboxd_url, '_blank')}
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
			class="font-display self-start pt-11 text-xs font-normal whitespace-nowrap uppercase"
			style="writing-mode: vertical-rl;"
		>
			Letterboxd Rating
		</p>
	</section>
</div>
