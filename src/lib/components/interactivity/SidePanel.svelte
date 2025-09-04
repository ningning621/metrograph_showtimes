<!--
  @component SidePanel - A side panel component based on HTML dialog
	@slot default - The inner content of the side panel, inside of the outer backdrop and wrapper
 -->

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Dialog from './Dialog.svelte';

	/** @type {Side} [side="right"] - side from which side panel should open */
	interface Props {
		side: 'top' | 'right' | 'bottom' | 'left';
		show?: () => void;
		close?: () => void;
		toggle?: () => void;
		children?: import('svelte').Snippet<[any]>;
		[key: string]: any;
	}

	let { side = 'right', children, ...rest }: Props = $props();

	let open: boolean = $state();

	const dispatch = createEventDispatcher();

	export const show = () => {
		dispatch('show');
		open = true;
	};
	export const close = () => {
		dispatch('close');
		open = false;
	};
	export const toggle = () => {
		dispatch('toggle');
		open = !open;
	};
</script>

<!-- {#if open}
	<div class="side-panel {side} contents">
		<Dialog {...rest} bind:open>
			{@render children?.({ show, close })}
		</Dialog>
	</div>
{/if} -->
