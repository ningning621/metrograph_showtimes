<script lang="ts">
	import md from '$lib/utils/md';
	import films from '$lib/data/films.csv';

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

<div class="content-well">
	<header class="mb-8 w-full py-6">
		<h1 class="text-center text-xl font-bold">Metrograph Weekly</h1>
	</header>

	<section class="flex justify-center">
		<table class="table">
			<thead>
				<!-- <tr>
					<th>Event</th>
					<th>Title</th>
					<th>Directors</th>
					<th>Letterboxd Rating</th>
				</tr> -->
			</thead>
			<tbody>
				{#each films.sort((a, b) => b.rating - a.rating) as film}
					<tr
						class="cursor-pointer hover:bg-gray-100"
						on:click={() => window.open(film.imageUrl, '_blank')}
					>
						<td class=" pr-2">{film.event_time_date ? '*' : ''}</td>

						<td class="pt-1.25 pr-2 align-top">
							<img src={film.imageUrl} alt={film.title} class="aspect-video w-8" /></td
						>
						<td class="py-px pr-2">{film.title}</td>
						<td class="px-2">{parseDirectors(film.directors)}</td>
						<td class="px-2">{film.rating}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</section>
</div>
