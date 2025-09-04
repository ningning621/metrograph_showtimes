<script lang="ts" module>
	// hostnames for common social platforms + our selected icon
	const hostnames = new Map([
		['twitter.com', 'mdi:twitter'],
		['facebook.com', 'mdi:facebook'],
		['instagram.com', 'mdi:instagram'],
		['linkedin.com', 'mdi:linkedin'],
		['github.com', 'mdi:github'],
		['github.dev', 'mdi:github'],
		['youtube.com', 'mdi:youtube'],
		['twitch.tv', 'mdi:twitch'],
		['twitch.com', 'mdi:twitch'],
		['discord.com', 'mdi:discord'],
		['discord.gg', 'mdi:discord'],
		['reddit.com', 'mdi:reddit']
	]);

	const getIcon = (href: string | undefined): string | undefined => {
		if (!href) return undefined;

		// catch common prompts
		if (href.startsWith('mailto:')) return 'mdi:email';
		else if (href.startsWith('tel:')) return 'mdi:phone';
		else if (href.startsWith('sms:')) return 'mdi:sms';

		// otherwise, check for a hostname match
		const parsedURL = new URL(href);
		if (!parsedURL) return undefined;

		// return the icon if it exists, otherwise undefined
		return hostnames?.get(parsedURL.hostname);
	};
</script>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import slugify from 'slugify';
	import Icon from '$lib/components/atoms/Icon.svelte';
	import keythrough from '$lib/actions/keythrough';
	import CopyURL from '../interactivity/CopyURL.svelte';

	/** @type {SocialItem[]} [items={$page.data.social}] - */

	/** @type {boolean} [copyLink=true] - enable/disabling copyLink component postfixed to list */
	interface Props {
		items?: SocialItem[];
		copyURL?: boolean;
		pre?: import('svelte').Snippet;
		item?: import('svelte').Snippet<[any]>;
		post?: import('svelte').Snippet;
		[key: string]: any;
	}

	let { items = [], copyURL = false, pre, item, post, ...rest }: Props = $props();

	const dispatch = createEventDispatcher();
</script>

<ul
	role="menubar"
	{...rest}
	class="flex flex-row gap-2 leading-none {rest.class}"
	use:keythrough={{ targets: '[role=menuitem]' }}
>
	{@render pre?.()}
	{#if items}
		{#each items as { title, url, icon, onClick } (url)}
			{@const slug = slugify(title, { lower: true, strict: true })}
			{@const parsedIcon = icon || getIcon(url)}
			{#if title && (url || onClick) && parsedIcon}
				<li role="none">
					{#if item}{@render item({ title, url, icon: parsedIcon })}{:else}
						<svelte:element
							this={url ? 'a' : 'button'}
							class="button md pill primary"
							role="menuitem"
							tabindex="0"
							{title}
							href={url}
							rel="noopener noreferrer"
							target="_blank"
							onclick={() => {
								if (url) return;
								dispatch(slug, { title, url, icon, onClick });
							}}
						>
							{#if parsedIcon}
								<Icon icon={parsedIcon} />
							{/if}
						</svelte:element>
					{/if}
				</li>
			{/if}
		{/each}
		{#if copyURL}
			<li role="none">
				<CopyURL them role="menuitem" tabindex={0} />
			</li>
		{/if}
	{/if}
	{@render post?.()}
</ul>
