<script lang="ts" module>
	// TODO: Add project-specific icons here to be able to use them in this component.
	const icons = {
		close: 'mdi:close',
		'arrow-right': 'mdi:arrow-right',
		menu: 'mdi:menu',
		'chevron-down': 'mdi:chevron-down',
		search: 'mdi:magnify',
		delete: 'mdi:delete',
		'view-grid': 'mdi:view-grid',
		'link-variant': 'mdi:link-variant',
		check: 'mdi:check'
	} as const;

	export type IconOptions = keyof typeof icons;
</script>

<script lang="ts">
	import type { IconProps } from '@iconify/svelte';

	interface Props extends IconProps {
		icon: IconOptions;
		class?: Classes;
		noobserver?: boolean;
		[key: string]: any;
	}

	let { icon, class: classes = '', noobserver = true, ...rest }: Props = $props();
</script>

<iconify-icon icon={icons[icon as IconOptions] || icon} class={classes} {noobserver} {...rest}
></iconify-icon>
