<script>
	import { page } from '$app/stores';
	import Button from '$lib/components/interactivity/Button.svelte';

	const errorTitles = new Map([
		[404, 'Page not found'],
		[500, 'Server error'],
		[503, 'Service unavailable']
	]);

	let h1 = $derived(
		errorTitles?.get($page.status) || $page?.error?.message || 'Something went wrong'
	);

	$inspect(`${$page?.status + ': ' + $page?.error?.message}`);
</script>

<section
	class="min-h-screen-minus-masthead-colophon relative grid h-full w-full flex-1 place-content-center text-center"
>
	<p class="eyebrow text-tertiary mb-2">{$page.status}</p>
	<h1 class="mb-1 text-6xl leading-none font-bold">
		{h1}
	</h1>
	<Button href="/" class="mx-auto mt-8 w-fit flex-row-reverse" icon={{ icon: 'ion:arrow-back' }}
		>Return to the homepage</Button
	>
</section>
