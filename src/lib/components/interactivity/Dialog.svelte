<script lang="ts">
	import type { Snippet } from 'svelte';
	import { Dialog } from 'bits-ui';
	import Icon from '$lib/components/atoms/Icon.svelte';

	interface Props {
		trigger: Snippet;
		title?: string | Snippet;
		description?: string | Snippet;
		content: Snippet;
		placement?: 'center' | 'left' | 'right';
	}

	let { trigger, title, description, content, placement = 'center' }: Props = $props();
</script>

<Dialog.Root>
	<Dialog.Trigger class="cursor-pointer">
		{@render trigger?.()}
	</Dialog.Trigger>
	<Dialog.Portal>
		<Dialog.Overlay
			class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 fixed inset-0 z-50 backdrop-blur-sm"
		/>
		<Dialog.Content
			class={[
				'bg-primary data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 border-primary fixed z-50 max-h-[95vh] overflow-y-auto rounded-sm border p-5 shadow-sm',
				placement === 'center' &&
					'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 top-1/2 left-1/2 w-[95vw] max-w-2xl -translate-x-1/2 -translate-y-1/2',
				placement === 'left' &&
					'data-[state=closed]:slide-out-to-left-4 data-[state=open]:slide-in-from-left-4 top-1/2 left-4 h-[95vh] w-[450px] max-w-[calc(100vw-2rem)] -translate-y-1/2',
				placement === 'right' &&
					'data-[state=closed]:slide-out-to-right-4 data-[state=open]:slide-in-from-right-4 top-1/2 right-4 h-[95vh] w-[450px] max-w-[calc(100vw-2rem)] -translate-y-1/2'
			]}
		>
			{#if title}
				<!-- Add margin right to account for close button at the top right -->
				<Dialog.Title class="mr-8">
					{#if typeof title === 'string'}
						<p class="headline-4 mb-2 font-bold">{title}</p>
					{:else}
						{@render title?.()}
					{/if}
				</Dialog.Title>
			{/if}
			{#if description}
				<Dialog.Description>
					{#if typeof description === 'string'}
						<p class="body-1 mb-2">{description}</p>
					{:else}
						{@render description?.()}
					{/if}
				</Dialog.Description>
			{/if}
			{@render content?.()}
			<Dialog.Close
				class="hover:bg-secondary active:bg-secondary label-1 absolute top-5 right-5 flex cursor-pointer items-center justify-center rounded-md p-1"
			>
				<Icon icon="close" class="text-icon-primary" />
				<span class="sr-only">Close</span>
			</Dialog.Close>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
