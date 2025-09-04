<script lang="ts">
	import Details from '$lib/components/layout/Details.svelte';

	const items = [
		{
			title: 'What is the meaning of life?',
			content:
				'To become a better person, to help others, and to leave the world a better place than you found it.'
		},
		{
			title: 'How do I become a better person?',
			content: 'Read books, listen to podcasts, and surround yourself with people who inspire you.'
		},
		{
			title: 'What is the best way to help others?',
			content: 'Give them your time, attention, and love.'
		}
	];
</script>

<Details {items} />
