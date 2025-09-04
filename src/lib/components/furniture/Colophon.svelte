<!--
  @component A footer to be applied in a +layout.svelte.
  There is heavy usage of aria attributes to ensure accessibility, so be careful when changing element IDs or aria attributes.
  @link {@see https://www.deque.com/|Deque's footer for an example of a footer}
-->
<script lang="ts" module>
	import { writable } from 'svelte/store';
	export const height = writable(198);
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import site from '$lib/site.yaml';
	import ShareBar from './ShareBar.svelte';

	let mounted = $state(false);
	onMount(() => (mounted = true));

	$effect(() => {
		if (browser && mounted) {
			document.documentElement.style.setProperty('--colophon-height', `${$height}px`);
		}
	});
</script>

<nav aria-labelledby="colophon-skip-links" class="sr-only">
	<h2 id="colophon-skip-links">Footer Skip Links</h2>
	<ul>
		<li><a href="#site-information">Skip to Site Information</a></li>
		<li><a href="#page-top">Skip to Top</a></li>
	</ul>
</nav>

<!-- svelte-ignore a11y_no_redundant_roles -->
<footer
	id="colophon"
	role="contentinfo"
	aria-labelledby="site-index-label"
	class="bg-secondary text-primary p-8"
	bind:offsetHeight={$height}
>
	<h2 id="site-index-label" class="sr-only">Site Index</h2>

	<div class="flex flex-row flex-wrap justify-between gap-x-8 gap-y-2">
		<!-- FOR SITE CONTENT PAGES -->
		<section id="site-content" aria-labelledby="site-content-label" class="contents">
			<h3 id="site-content-label" class="sr-only">Site Content</h3>

			<div class="w-full text-3xl font-semibold">
				<a href="/" rel="home" data-sveltekit-preload-data="hover">
					{site.title}
				</a>
			</div>

			<!--
				SITE CONTENT LINKS IN HERE
      	if grouped, apply an h4 tag with an appropriate heading for each group
   		 -->
			<section>
				<ul class="flex flex-row flex-wrap gap-x-4 gap-y-2">
					<li><a href="/">Route #1</a></li>
					<li><a href="/">Route #2</a></li>
					<li><a href="/">Route #3</a></li>
				</ul>
			</section>
		</section>

		<!-- SOCIAL MEDIA FOR PUBLISHER -->
		<!-- PROPOGATES FROM METADATA -->
		{#if site.social.length}
			<nav id="social-media-links" aria-labelledby="social-media-links-label">
				<h3 id="social-media-links-label" class="sr-only">Social Media Links</h3>
				<div>
					<ShareBar copyURL items={site.social} class="text-xl" />
				</div>
			</nav>
		{/if}
	</div>

	<hr class="border-secondary my-4" />

	<!-- FOR SITE INFORMATION -->
	<section
		id="site-information"
		aria-labelledby="site-information-label"
		class="text-tertiary flex flex-row flex-wrap items-center justify-between gap-x-8 gap-y-2 text-sm"
	>
		<h3 id="site-information-label" class="sr-only">Site Information</h3>

		<!-- SITE LEGAL INFORMATION LINKS -->
		<nav id="legal-links" aria-labelledby="site-legal-information" class="contents">
			<h3 id="site-legal-information" class="sr-only">Site Legal Information</h3>
			<!--
        SITE LEGAL INFORMATION
        EXAMPLE USAGE
      -->
			<ul class="flex flex-row flex-wrap gap-x-4 gap-y-2">
				<li><a href="/privacy">Privacy Policy</a></li>
				<li><a href="/terms">Terms of Use</a></li>
			</ul>
		</nav>

		<!-- SITE SHAREBAR & COPYRIGHT -->
		<div>
			<!-- MUST PROPOGATE FROM METADATA -->
			<p class="text-xs">
				<abbr class="no-underline" title="Copyright">©</abbr>
				{site.date_modified.getFullYear()}
				{site.publisher.name}
			</p>
		</div>
	</section>
</footer>
