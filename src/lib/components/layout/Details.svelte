<script lang="ts">
	import type { Snippet } from 'svelte';
	import md from '$lib/utils/md';

	import { Accordion } from 'bits-ui';
	import Icon from '$lib/components/atoms/Icon.svelte';

	interface Props {
		items: {
			value?: string;
			title: string;
			content: string;
		}[];
		type?: 'multiple' | 'single';
	}

	let { items, type = 'multiple' }: Props = $props();
</script>

<Accordion.Root class="w-full" {type}>
	{#each items as { value, title, content }, i (i)}
		<Accordion.Item value={value ?? `${i}`} class="border-primary group/item border-b px-2">
			<Accordion.Header>
				<Accordion.Trigger
					class="body-1 group/trigger flex w-full flex-1 cursor-pointer items-center justify-between py-4 [&[data-state=open]>.icon-wrapper>*]:rotate-180"
				>
					<span class="w-full text-left">
						{title}
					</span>
					<span
						class="icon-wrapper group-hover/trigger:bg-tertiary text-primary inline-flex size-8 items-center justify-center rounded-sm bg-transparent"
					>
						<Icon icon="chevron-down" class="transition-transform duration-200" />
					</span>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content
				class="data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down body-2 overflow-hidden"
			>
				<div class="pb-4">
					{@html md(content)}
				</div>
			</Accordion.Content>
		</Accordion.Item>
	{/each}
</Accordion.Root>
