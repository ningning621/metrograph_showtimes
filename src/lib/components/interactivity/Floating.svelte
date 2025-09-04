<script lang="ts">
	import {
		computePosition,
		shift,
		flip,
		offset,
		type ComputePositionConfig
	} from '@floating-ui/dom';

	interface Props {
		class?: string;
		maxWidth?: number;
		/** if undefined, will float using Window */
		relative?: HTMLElement | undefined;
		placement?: ComputePositionConfig['placement'];
		children?: import('svelte').Snippet;
	}

	let {
		class: classes = '',
		maxWidth = $bindable(350),
		relative = undefined,
		placement = 'right-start',
		children
	}: Props = $props();

	let innerWidth = $state(300);
	let floating: HTMLElement | undefined = $state();

	$effect(() => {
		if (relative && floating) {
			computePosition(relative, floating, {
				placement: placement,
				middleware: [offset(5), flip(), shift()],
				strategy: 'absolute'
			}).then(({ x, y, placement }) => {
				maxWidth = Math.min(placement.includes('left') ? x - 10 : innerWidth - x - 10, 240);
				if (!floating) return;
				Object.assign(floating.style, {
					top: `${y}px`,
					left: `${x}px`,
					opacity: 1,
					zIndex: 10
				});
			});
		}
	});
</script>

<svelte:window
	bind:innerWidth
	onmousemove={({ clientX, clientY }) => {
		if (relative || !floating) return;

		const virtualEl = {
			getBoundingClientRect() {
				return {
					width: 0,
					height: 0,
					x: clientX,
					y: clientY,
					left: clientX,
					right: clientX,
					top: clientY,
					bottom: clientY
				};
			}
		};

		computePosition(virtualEl, floating, {
			placement: 'right-start',
			middleware: [offset(5), flip(), shift()],
			strategy: 'fixed'
		}).then(({ x, y, placement }) => {
			maxWidth = Math.min(
				placement.includes('left') ? clientX - 10 : innerWidth - clientX - 10,
				240
			);
			if (!floating) return;

			Object.assign(floating.style, {
				top: `${y}px`,
				left: `${Math.max(0, x)}px`,
				opacity: 1,
				zIndex: 9999
			});
		});
	}}
/>

<div
	class="font-regular border-primary bg-primary pointer-events-none fixed z-40 flex w-auto min-w-[225px] flex-col gap-2 rounded-lg border px-3 py-2 text-left text-base opacity-0 shadow-md {classes}"
	style:max-width="{maxWidth}px"
	bind:this={floating}
>
	{@render children?.()}
</div>
