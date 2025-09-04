<script lang="ts">
	import Icon from '$lib/components/atoms/Icon.svelte';

	const classes = {
		background: ['bg-primary', 'bg-secondary', 'bg-tertiary', 'bg-accent', 'bg-offset'],
		text: [
			'text-primary',
			'text-secondary',
			'text-tertiary',
			'text-accent',
			'text-inactive',
			'text-offset'
		],
		icon: [
			'text-icon-primary',
			'text-icon-secondary',
			'text-icon-accent',
			'text-icon-inactive',
			'text-icon-offset'
		],
		border: [
			'border-primary',
			'border-secondary',
			'border-tertiary',
			'border-strong',
			'border-accent',
			'border-offset'
		]
	};
</script>

<div class="flex flex-col gap-y-8">
	{#each Object.keys(classes) as group}
		{@const groupClasses = classes[group as keyof typeof classes]}
		<div class="flex flex-col gap-y-2">
			<h3 class="headline-5 text-primary font-bold">{group}</h3>
			{#each ['scheme-light', 'scheme-dark'] as theme}
				<div class="flex flex-col gap-y-2 {theme} bg-primary rounded-sm p-2">
					<h4 class="body-1 text-primary font-bold">{theme}</h4>
					<div class="flex flex-row flex-wrap gap-2">
						{#each groupClasses as className}
							{#if group === 'background'}
								<div class="flex flex-col gap-y-1">
									<p class="body-4 text-primary">{className}</p>
									<div class="h-8 w-24 rounded-sm {className}"></div>
								</div>
							{:else if group === 'text'}
								<p class={className}>{className}</p>
							{:else if group === 'icon'}
								<div class="flex flex-col gap-y-1">
									<p class="body-4 text-primary">{className}</p>
									<Icon icon="close" class={className} />
								</div>
							{:else if group === 'border'}
								<div class="rounded-sm border p-2 {className}">
									<p class="body-4 text-primary">{className}</p>
								</div>
							{/if}
						{/each}
					</div>
				</div>
			{/each}
		</div>
	{/each}
</div>
