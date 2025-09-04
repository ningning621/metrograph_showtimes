<!--
  @component Modal - A modal dialog component
	@slot default - The inner content of the modal, inside of the outer backdrop and wrapper
	@slot prompt - The inner content of a button element, most simply a string
 -->
<script lang="ts">
	import { dev } from '$app/environment';
	import { onDestroy, onMount, tick } from 'svelte';
	import { backOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';
	import { createFocusTrap, type FocusTrap } from 'focus-trap';
	import { disableBodyScroll, clearAllBodyScrollLocks } from 'body-scroll-lock';
	import outclick from '$lib/actions/outclick';
	import { overlay } from '$lib/stores';
	import Icon from '$lib/components/atoms/Icon.svelte';

	interface Props {
		id?: string;
		labelledby?: string;
		describedby?: string;
		class?: string;
		children?: import('svelte').Snippet;
		closeButton?: import('svelte').Snippet<[any]>;
		[key: string]: any;
	}

	let {
		id,
		labelledby = '',
		describedby = '',
		class: classes = '',
		children,
		closeButton,
		...rest
	}: Props = $props();

	let el: HTMLDivElement | undefined = $state();
	let trap: FocusTrap | undefined = $state();
	let mounted = $state(false);

	const close = async () => {
		if (rest.onclose) rest.onclose();
	};

	onMount(async () => {
		mounted = true;
		overlay.set(true);

		await tick();

		if (!el) return;

		disableBodyScroll(el, {
			allowTouchMove: (node) => {
				while (node && node !== el && el?.contains(node)) {
					if (node.getAttribute('body-scroll-lock-ignore') !== null) {
						return true;
					}
					if (node.parentElement) node = node.parentElement;
				}
				return false;
			}
		});

		trap = createFocusTrap(el, {
			clickOutsideDeactivates: true,
			escapeDeactivates: true,
			initialFocus: el
		});
		trap?.activate();
	});

	onDestroy(async () => {
		if (!el || !mounted) return;
		overlay.set(false);

		await tick();

		clearAllBodyScrollLocks();
		trap?.deactivate();
		trap = undefined;
	});

	$effect(() => {
		if (dev) {
			if (!id) console.warn('[Modal.svelte] Required `id` is undefined.');
		}
	});
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div
	{id}
	aria-modal="true"
	role="dialog"
	aria-live="assertive"
	aria-labelledby={labelledby || undefined}
	aria-describedby={describedby || undefined}
	class="fixed inset-0 z-50 grid place-items-center p-8"
	in:fly={{ y: 15, duration: 200, delay: 75, easing: backOut }}
	bind:this={el}
	onkeydown={(e) => {
		switch (e.code) {
			case 'Escape':
				close();
				break;
		}
	}}
	{...rest}
>
	<div class="relative w-full max-w-2xl overflow-auto {classes}" use:outclick={close}>
		{#if closeButton}
			{@render closeButton?.(id)}
		{:else}
			<button
				aria-controls={id}
				class="bg-primary text-icon-secondary hover:bg-secondary hover:text-primary focus:bg-secondary focus:text-primary active:bg-tertiary absolute top-0 right-0 z-50 rounded-bl p-1 leading-none"
				onclick={close}
			>
				<span class="sr-only">Close modal</span>
				<Icon class="text-lg" icon="close" aria-hidden="true" />
			</button>
		{/if}

		<div body-scroll-lock-ignore>
			{@render children?.()}
		</div>
	</div>
</div>
