<script lang="ts">
	import Dropdown from '$lib/components/interactivity/Dropdown.svelte';

	type DropdownItem = {
		value: string;
		label: string;
		disabled?: boolean;
	};

	const items: DropdownItem[] = [
		{ value: 'apple', label: 'Apple' },
		{ value: 'banana', label: 'Banana' },
		{ value: 'cherry', label: 'Cherry' },
		{ value: 'grape', label: 'Grape' },
		{ value: 'orange', label: 'Orange', disabled: true }
	];

	let value1 = $state<DropdownItem | undefined>(undefined);
	let value2 = $state<DropdownItem[] | undefined>(undefined);
	let value3 = $state<DropdownItem | undefined>(undefined);

	$inspect(value1);
</script>

<div
	class="border-tertiary flex w-full flex-row flex-wrap items-center justify-around rounded-sm border border-dashed p-8"
>
	<div class="flex flex-col gap-2">
		<p class="font-semibold">Default dropdown</p>
		<Dropdown {items} bind:value={value1} class="w-[300px]"></Dropdown>
		<p>Selected value: {value1}</p>
	</div>

	<div class="flex flex-col gap-2">
		<p class="font-semibold">Dropdown with multi-select</p>
		<Dropdown {items} bind:value={value2} type="multiple" class="w-[300px]"></Dropdown>
		<p>Selected value: {value2 ? value2.join(', ') : ''}</p>
	</div>

	<div class="flex flex-col gap-2">
		<p class="font-semibold">Dropdown with search</p>
		<Dropdown {items} bind:value={value3} hasSearch={true} class="w-[300px]"></Dropdown>

		<p>Selected value: {value3}</p>
	</div>
</div>
