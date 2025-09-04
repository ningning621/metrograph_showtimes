<script module>
	type DropdownItem = {
		label: string;
		value: string;
	};
</script>

<script lang="ts">
	import { Combobox } from 'bits-ui';
	import Icon from '$lib/components/atoms/Icon.svelte';

	interface Props {
		value?: string | string[];
		items: DropdownItem[];
		hasSearch?: boolean;
		type?: 'single' | 'multiple';
		placeholder?: string;
		class?: string;
		[key: string]: any;
	}

	let {
		value = $bindable(undefined),
		items = [],
		hasSearch = false,
		type = 'single',
		placeholder = 'Select...',
		class: classes = ''
	}: Props = $props();

	// Based on the selected values, get the full items that are selected to use their labels in the input.
	let selectedItems = $derived(
		items.filter((item) =>
			Array.isArray(value) ? value.includes(item.value) : value === item.value
		)
	);

	// The Combobox component anchors the dropdown to the input by default, but in this case there may not be a default if search is disabled. So we'll anchor this to a custom element to make sure the dropdown is always visible.
	let customAnchor = $state<HTMLElement>(null!);

	// Search functionality to filter items shown if search is enabled.
	let searchValue = $state('');

	const filteredItems = $derived(
		searchValue === ''
			? items
			: items.filter(({ label }) => label.toLowerCase().includes(searchValue.toLowerCase()))
	);
</script>

<Combobox.Root
	{type}
	name="selected"
	bind:value
	onOpenChange={(o) => {
		if (!o) searchValue = '';
	}}
>
	<div class="h-full w-full" bind:this={customAnchor}>
		<Combobox.Trigger
			class={[
				'border-primary bg-background hover:border-offset focus:border-offset relative flex h-auto w-[200px] cursor-pointer touch-none flex-row items-center justify-between gap-2 rounded-lg border px-3 py-2 transition-colors select-none',
				classes
			]}
		>
			{#if hasSearch}
				<Icon icon="search" class="body-1" />
				<Combobox.Input
					oninput={(e) => (searchValue = e.currentTarget.value)}
					class="h-input focus inline-flex w-full touch-none truncate transition-colors"
					{placeholder}
					aria-label={placeholder}
				/>
			{:else}
				<div class="flex w-full flex-row items-center gap-2 truncate">
					{selectedItems.length > 0 ? selectedItems.map((d) => d.label).join(', ') : placeholder}
				</div>
			{/if}
			<Icon icon="chevron-down" class="body-1 pointer-events-none" />
		</Combobox.Trigger>
	</div>

	<Combobox.Portal>
		<Combobox.Content
			class="focus-override border-offset data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 bg-primary z-50 h-fit max-h-[var(--bits-select-content-available-height)] w-[var(--bits-select-anchor-width)] min-w-[var(--bits-select-anchor-width)] cursor-pointer rounded-xl border px-0 py-3 shadow-sm outline-hidden select-none data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1"
			sideOffset={10}
			{customAnchor}
		>
			<div class="w-[300px]">
				<Combobox.Viewport>
					{#each filteredItems as item, i (i + item.value)}
						<Combobox.Item
							class="bg-primary data-highlighted:bg-tertiary flex h-10 w-full items-center px-2 capitalize outline-hidden select-none"
							value={item.value}
							label={item.label}
						>
							{#snippet children({ selected })}
								{item.label}
								{#if selected}
									<div class="ml-auto">
										<Icon icon="check" class="body-1 pointer-events-none relative" />
									</div>
								{/if}
							{/snippet}
						</Combobox.Item>
					{:else}
						<span class="block px-2 py-1 text-sm text-tertiary">No results found, try again.</span>
					{/each}
				</Combobox.Viewport>
			</div>
		</Combobox.Content>
	</Combobox.Portal>
</Combobox.Root>
