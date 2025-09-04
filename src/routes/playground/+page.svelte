<script lang="ts">
	import Section from './Section.svelte';
	import TailwindColors from './sections/TailwindColors.svelte';
	import Button from './sections/Button.svelte';
	import Dialog from './sections/Dialog.svelte';
	import Dropdown from './sections/Dropdown.svelte';
	import Details from './sections/Details.svelte';
	import Toggle from './sections/Toggle.svelte';

	const sections = {
		tailwindColors: {
			title: 'Tailwind Color Variables',
			description:
				'Tailwind variables are set in tokens.css and are used to define the colors in the project. They change depending on the theme of their container. Below are examples of those variables in context.',
			component: TailwindColors
		},
		button: {
			title: 'Button',
			description: 'Different types of buttons.',
			component: Button
		},
		dialog: {
			title: 'Dialog',
			description: 'A dialog is a modal window that appears in front of the current page.',
			component: Dialog
		},
		search: {
			title: 'Dropdown',
			description: 'Different types of dropdowns.',
			component: Dropdown
		},
		details: {
			title: 'Details',
			description: 'A details component with expandable sections, usually used for FAQs.',
			component: Details
		},
		toggle: {
			title: 'Toggle',
			description: 'Different types of toggles.',
			component: Toggle
		}
	};
</script>

<!-- Hero Header -->
<section class="bg-primary text-primary border-primary border-b">
	<div class="content-well py-12">
		<h1 class="headline-1 mb-4 font-bold">Component Playground</h1>
		<p class="body-1 text-secondary max-w-2xl">
			Explore and test the components in this project. Each section demonstrates different
			components with examples and documentation for their usage.
		</p>
	</div>
</section>

<!-- Sticky Navigation -->
<nav class="bg-primary border-primary sticky top-0 z-10 border-b">
	<div class="content-well py-4">
		<div class="flex items-center gap-1 overflow-x-auto">
			<span class="eyebrow-2 text-tertiary mr-4 font-medium whitespace-nowrap">Jump to:</span>
			{#each Object.keys(sections) as section}
				<a href="#{section}" class="button pill primary sm">
					{sections[section as keyof typeof sections].title}
				</a>
			{/each}
		</div>
	</div>
</nav>

<!-- Main Content -->
<main class="bg-primary">
	{#each Object.keys(sections) as section, index}
		{@const sectionInfo = sections[section as keyof typeof sections]}
		<div class="relative py-12">
			<Section id={section} title={sectionInfo.title} description={sectionInfo.description}>
				<svelte:component this={sectionInfo.component} />
			</Section>
		</div>
	{/each}
</main>
