<script lang="ts">
	import { Button } from 'bits-ui';
	import Icon from '$lib/components/atoms/Icon.svelte';
	import type { IconOptions } from '$lib/components/atoms/Icon.svelte';

	interface Props {
		class?: Classes;
		size?: 'sm' | 'md' | 'lg';
		color?: 'primary' | 'accent';
		variant?: 'pill' | 'underlined';
		icon?: IconOptions;
		iconSide?: 'left' | 'right';
		disabled?: boolean;
		[key: string]: any;
	}

	let {
		class: classes = '',
		children,
		size = 'md',
		color = 'primary',
		variant = 'pill',
		icon,
		iconSide = 'right',
		disabled = false,
		...rest
	}: Props = $props();

	let isExternal = $derived(rest?.href?.startsWith('http') || rest?.href?.startsWith('www'));
</script>

<Button.Root
	class={['button group', iconSide === 'left' && 'flex-row-reverse', size, color, variant, classes]}
	{disabled}
	target={isExternal ? '_blank' : '_self'}
	{...rest}
>
	{@render children?.()}
	{#if icon}
		<Icon {icon} class="icon"></Icon>
	{/if}
</Button.Root>
