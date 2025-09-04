<script lang="ts">
	import { ToggleGroup } from 'bits-ui';

	interface Props {
		value: string[];
		items: string[];
		type?: 'single' | 'multiple';
		class?: string;
	}

	let { value = $bindable(), items = [], type = 'single', class: classes = '' }: Props = $props();
</script>

<ToggleGroup.Root bind:value {type} class={['flex items-center gap-x-2', classes]}>
	{#each items as item}
		<ToggleGroup.Item
			aria-label="toggle {item}"
			value={item}
			class="data-[state=on]:text-offset data-[state=on]:bg-offset data-[state=off]:bg-tertiary data-[state=off]:text-tertiary inline-flex size-10 w-fit cursor-pointer items-center justify-center rounded-full px-4 transition-all hover:scale-[1.05]"
		>
			<span>{item}</span>
		</ToggleGroup.Item>
	{/each}
</ToggleGroup.Root>
