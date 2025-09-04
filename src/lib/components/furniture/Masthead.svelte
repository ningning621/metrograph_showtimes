<script module lang="ts">
	export const height: { value: number } = $state({ value: 72 });
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { MediaQuery } from 'svelte/reactivity';

	import Icon from '$lib/components/atoms/Icon.svelte';
	import { NavigationMenu } from 'bits-ui';
	import Dialog from '$lib/components/interactivity/Dialog.svelte';

	import site from '$lib/site.yaml';

	const isDesktop = new MediaQuery('(min-width: 768px)');

	$effect(() => {
		if (browser && document) {
			document.documentElement.style.setProperty('--masthead-height', `${height.value}px`);
		}
	});
</script>

<header id="masthead" class="bg-primary border-primary border-b">
	<a href="#main-content" class="sr-only">Skip to main content</a>
	<div
		class="text-primary content-well flex flex-row flex-wrap items-center justify-between gap-2 py-2"
		bind:offsetHeight={height.value}
	>
		<a href="/" rel="home">
			<span class="sr-only">{site.title}</span>
			<enhanced:img src="$lib/assets/logo.png" alt={site.title} class="w-16" />
		</a>

		{#if isDesktop.current}
			<NavigationMenu.Root class="relative" aria-label="Main navigation">
				<NavigationMenu.List class="flex items-center gap-x-4">
					{#each site.links as { title, href, parent, links }}
						<NavigationMenu.Item class="hover:bg-secondary body-2 px-2 py-1">
							{#if !parent}
								<NavigationMenu.Link class="cursor-pointer" {href}>{title}</NavigationMenu.Link>
							{:else}
								<NavigationMenu.Trigger
									class="group flex cursor-pointer items-center justify-center gap-1"
								>
									<span>{parent}</span>
									<Icon icon="chevron-down" class="transition-transform group-hover:rotate-180" />
								</NavigationMenu.Trigger>
								<NavigationMenu.Content
									class="data-[motion=from-end]:animate-enter-from-right data-[motion=from-start]:animate-enter-from-left data-[motion=to-end]:animate-exit-to-right data-[motion=to-start]:animate-exit-to-left absolute top-0 left-0 w-full sm:w-auto"
								>
									<ul class="flex w-[200px] flex-col gap-4 p-4">
										{#each links as link (link.title)}
											<li>
												<NavigationMenu.Link
													href={link.href}
													class="hover:bg-secondary flex w-full flex-row items-center justify-between p-2"
												>
													<p>{link.title}</p>
													<Icon icon="arrow-right" />
												</NavigationMenu.Link>
											</li>
										{/each}
									</ul>
								</NavigationMenu.Content>
							{/if}
						</NavigationMenu.Item>
					{/each}
				</NavigationMenu.List>
				<div class="absolute top-full left-0 flex w-full justify-center perspective-[2000px]">
					<NavigationMenu.Viewport
						class="bg-primary data-[state=closed]:animate-scale-out data-[state=open]:animate-scale-in border-primary relative mt-2 h-[var(--bits-navigation-menu-viewport-height)] w-full origin-[top_center] overflow-hidden rounded-sm border shadow-lg transition-[width,_height] duration-200 sm:w-[var(--bits-navigation-menu-viewport-width)]"
					/>
				</div>
			</NavigationMenu.Root>
		{:else}
			<Dialog placement="right">
				{#snippet title()}
					<a href="/" rel="home">
						<span class="sr-only">{site.title}</span>
						<enhanced:img src="$lib/assets/logo.png" alt={site.title} class="w-16" />
					</a>
				{/snippet}
				{#snippet trigger()}
					<div class="hover:bg-secondary flex items-center justify-center rounded-sm p-1">
						<Icon icon="menu" class="label-1" />
						<span class="sr-only">Menu</span>
					</div>
				{/snippet}
				{#snippet content()}
					<NavigationMenu.Root aria-label="Main navigation menu">
						<NavigationMenu.List class="flex flex-col gap-y-6 py-4">
							{#each site.links as { title, href, parent, links }}
								{#if !parent}
									<NavigationMenu.Item>
										<NavigationMenu.Link class="dialog-navigation-link" {href}>
											<p>{title}</p>
											<Icon icon="arrow-right" />
										</NavigationMenu.Link>
									</NavigationMenu.Item>
								{:else}
									<div class="flex flex-col gap-y-6">
										<p class="label-3 text-secondary font-bold uppercase">{parent}</p>
										<ul class="flex flex-col gap-y-6">
											{#each links as link (link.title)}
												<li>
													<NavigationMenu.Item>
														<NavigationMenu.Link href={link.href} class="dialog-navigation-link">
															<p>{link.title}</p>
															<Icon icon="arrow-right" />
														</NavigationMenu.Link>
													</NavigationMenu.Item>
												</li>
											{/each}
										</ul>
									</div>
								{/if}
							{/each}
						</NavigationMenu.List>
					</NavigationMenu.Root>
				{/snippet}
			</Dialog>
		{/if}
	</div>
</header>

<style lang="postcss" type="postcss">
	@reference '$lib/styles/app.css';

	:global(.dialog-navigation-link) {
		@apply border-secondary hover:border-primary flex w-full flex-row items-center justify-between border-b;
	}
</style>
